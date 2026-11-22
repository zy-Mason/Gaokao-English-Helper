# Copyright (C) 2026 Mason 朱懿
import asyncio
import json
import os
import random

from .ai import ask_ai_notool
from .filex import DATA_DIR, get_file_object
from .prompt import ranker

# 每组词条数，一次问太多模型容易迷失
BATCH_SIZE = 25
# 重复打分轮数，每轮重新随机分组，最后取各轮平均分
ROUNDS = 3
# 同时进行的打分请求数，太高容易触发接口限流
MAX_CONCURRENCY = 50
# 模型返回条数不符时的最大尝试次数（含首次请求），避免无限重发
MAX_ATTEMPTS = 3


def _loads_object(text: str) -> dict:
    """容错解析模型返回：忽略代码围栏等前后缀，截取最外层 JSON 对象。"""
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end <= start:
        raise ValueError(f"模型没有返回 JSON 对象：{text[:200]}")
    return json.loads(text[start:end + 1])


def _parse_score(value) -> int:
    """把模型给的分数规范成 1-10 的整数。"""
    try:
        score = int(float(value))
    except (TypeError, ValueError):
        raise ValueError(f"无法解析的分数：{value!r}")
    return min(10, max(1, score))


async def _score_batch(batch: list) -> list:
    """把一批词条交给模型打分，返回与 batch 等长、顺序一致的整数分数列表。

    模型返回条数不一致（含返回内容无法解析出 items）时，把这次回答接进
    原有对话并提醒它重发，最多尝试 MAX_ATTEMPTS 次，仍不合格才抛异常。
    """
    payload = [{"en": item["en"], "zh": item["zh"]} for item in batch]
    messages = [
        {"role": "system", "content": ranker},
        {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
    ]
    attempt = 1
    while True:
        answer = await ask_ai_notool(messages, reasoning_effort="low",
                                     response_format="json_object")
        print("模型完成这个问答")
        content = answer.content or ""
        try:
            result = _loads_object(content)["items"]
            if len(result) != len(batch):
                raise ValueError(
                    f"你返回了 {len(result)} 项，与输入的 {len(batch)} 项不一致")
            # 数量和顺序已校验，只取模型的 score，en 和 zh 保留原文
            return [_parse_score(res.get("score")) for res in result]
        except (ValueError, KeyError, AttributeError) as exc:
            reason = str(exc)
        if attempt >= MAX_ATTEMPTS:
            raise ValueError(f"打分共尝试 {attempt} 次仍不合格：{reason}")
        print(f"  模型返回不合格（{reason}），接上对话重发第 {attempt + 1}/{MAX_ATTEMPTS} 次")
        # 接上原有对话：不合格的回答留在上下文里，再用 user 消息要求重发
        if content:
            messages.append({"role": "assistant", "content": content})
        messages.append({"role": "user", "content": (
            f"{reason}。请严格按输入顺序，原样输出全部 {len(batch)} 项，"
            f"每项只包含 en、zh、score，只输出一个 JSON 对象。")})
        attempt += 1


async def score_items(items: list) -> list[dict]:
    """
    list[dict]：返回与传入列表等长、顺序一致的新列表，每个元素是原词条的一份副本，但额外带上了 "score" 键。
    随机分组、重复 ROUNDS 轮打分后取平均，返回带一位小数 score 的新列表。
    每轮把所有词条重新随机打乱后按 BATCH_SIZE 切组，所有组并发请求（受
    MAX_CONCURRENCY 限制），各轮分数求平均；不改动传入的列表。
    """
    if not items:
        return []
    totals = [0] * len(items)
    semaphore = asyncio.Semaphore(MAX_CONCURRENCY)
    groups = []
    for round_index in range(1, ROUNDS + 1):
        order = list(range(len(items)))
        random.shuffle(order)
        group_count = (len(order) + BATCH_SIZE - 1) // BATCH_SIZE
        print(f"打分第 {round_index}/{ROUNDS} 轮：{len(order)} 个词条，共 {group_count} 组")
        for group_index, start in enumerate(range(0, len(order), BATCH_SIZE), 1):
            groups.append((round_index, group_index, group_count,
                           order[start:start + BATCH_SIZE]))

    async def run(round_index, group_index, group_count, group):
        async with semaphore:
            print(f"  第 {round_index} 轮 {group_index}/{group_count} 组（{len(group)} 个）……")
            return await _score_batch([items[i] for i in group])

    # 所有轮次、所有组一起入队，信号量控制实际并发数
    results = await asyncio.gather(*(run(*group) for group in groups))
    for (_, _, _, group), scores in zip(groups, results):
        for i, score in zip(group, scores):
            totals[i] += score
    return [{**item, "score": round(total / ROUNDS, 1)}
            for item, total in zip(items, totals)]


async def rank_json(sourecjsonpath: str | None = None) -> list:
    """sourecjsonpath是源json路径，如果为空则默认data/json/word.json
    读取 json（默认 data/json/word.json），给未打分的词条打分并写回，返回全部词条。
    词条形如 {"en": ..., "zh": ..., "score": ...}，score 是多轮打分后保留一位小数的
    平均分；已带合法 score 的词条会跳过，所以重复运行不会重复请求模型。
    """
    if sourecjsonpath is None:
        sourecjsonpath = os.path.join(DATA_DIR, "json", "word.json")
    with get_file_object(sourecjsonpath, "r") as datafile:
        text = datafile.read()
    if not text.strip():
        return []
    items = json.loads(text)["items"]
    todolist = [i for i, item in enumerate(items) if not isinstance(item.get("score"), (int, float))]
    # todolist 是一个下标列表，比如 [0, 3, 7]，表示第 0、3、7 个词条需要打分
    if todolist:
        print(f"待打分词条 {len(todolist)} 个，{len(items) - len(todolist)} 个已有分数跳过")
        ranked = await score_items([items[i] for i in todolist])
        for i, item in zip(todolist, ranked):
            items[i] = item
        # 全量写回，保持与 process_images 相同的格式
        with get_file_object(sourecjsonpath, "w") as datafile:
            json.dump({"items": items}, datafile, ensure_ascii=False, indent=4)
        print(f"分数已写回：{sourecjsonpath}")
    else:
        print("所有词条都已打过分，无需重复请求模型")
    return items

__all__ = ["rank_json"]
