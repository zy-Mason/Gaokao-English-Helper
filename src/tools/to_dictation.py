# Copyright (C) 2026 Mason 朱懿
import asyncio
import json
import math
import os
import re

from .ai import ask_ai_notool
from .filex import get_file_object, md_to_pdf
from .prompt import translator

# 加粗片段（**...**），非贪婪匹配，逐个加横线
BOLD_PATTERN = re.compile(r"\*\*(.+?)\*\*")
# 横线长度与加粗部分可见字符数（不计空白）的比例，0.5 时大致是半个词长
UNDERLINE_RATIO = 0.5
# 横线的最短长度，保证很短的加粗词也有可写的空
MIN_UNDERLINE = 4
# 模型返回不合格时的最大尝试次数（含首次请求）
MAX_ATTEMPTS = 3


def add_blanks(text: str) -> str:
    """在每个加粗片段后面补上带序号的横线，返回处理后的文本。

    形如 **Crowds jammed the entrance** 1.___________to Voss Dynamics，
    横线长度随加粗部分长度变化，序号在全文内依次递增。
    """
    number = 0

    def replace(match: re.Match) -> str:
        nonlocal number
        number += 1
        # 按可见字符数（不计空白）折算，避免长短语撑出一整行横线
        length = len(re.sub(r"\s", "", match.group(1)))
        underscores = max(MIN_UNDERLINE, math.ceil(length * UNDERLINE_RATIO))
        return f"{match.group(0)} {number}.{'_' * underscores} "

    return BOLD_PATTERN.sub(replace, text)


def dictation(md_path: str) -> str:
    """给 md 里每个加粗英文后面加默写横线，落盘到同目录，返回新 md 路径。

    :param md_path: 原始 md 路径，通常是 draft_story 生成的故事
    :return: 默写版 md 路径（原文件名加 _dictation 后缀）
    """
    if not os.path.isfile(md_path):
        raise FileNotFoundError(f"文件不存在: {md_path}")

    with get_file_object(md_path, "r") as datafile:
        text = datafile.read()

    base, ext = os.path.splitext(md_path)
    new_mdpath = f"{base}_dictation{ext}"
    with get_file_object(new_mdpath, "w") as datafile:
        datafile.write(add_blanks(text))
    print(f"默写版 Markdown 已保存：{new_mdpath}")
    return new_mdpath


def _loads_object(text: str) -> dict:
    """容错解析模型返回：忽略代码围栏等前后缀，截取最外层 JSON 对象。"""
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end <= start:
        raise ValueError(f"模型没有返回 JSON 对象：{text[:200]}")
    return json.loads(text[start:end + 1])


async def _translate(phrases: list[str]) -> dict[str, str]:
    """把加粗英文批量交给模型翻译，返回 {英文原文: 中文} 的映射。

    模型返回条数不一致或缺译文时，把这次回答接进对话要求重发，
    最多尝试 MAX_ATTEMPTS 次，仍不合格才抛异常。
    """
    payload = [{"en": phrase} for phrase in phrases]
    messages = [
        {"role": "system", "content": translator},
        {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
    ]
    attempt = 1
    while True:
        answer = await ask_ai_notool(messages, reasoning_effort="low",
                                     response_format="json_object")
        content = answer.content or ""
        try:
            result = _loads_object(content)["items"]
            if len(result) != len(phrases):
                raise ValueError(
                    f"你返回了 {len(result)} 项，与输入的 {len(phrases)} 项不一致")
            mapping = {}
            for phrase, item in zip(phrases, result):
                zh = str(item.get("zh") or "").strip()
                if not zh:
                    raise ValueError(f"第 {len(mapping) + 1} 项缺少中文译文")
                mapping[phrase] = zh
            return mapping
        except (ValueError, KeyError, AttributeError) as exc:
            reason = str(exc)
        if attempt >= MAX_ATTEMPTS:
            raise ValueError(f"翻译共尝试 {attempt} 次仍不合格：{reason}")
        print(f"  模型返回不合格（{reason}），接上对话重发第 {attempt + 1}/{MAX_ATTEMPTS} 次")
        if content:
            messages.append({"role": "assistant", "content": content})
        messages.append({"role": "user", "content": (
            f"{reason}。请严格按输入顺序，原样输出全部 {len(phrases)} 项，"
            f"每项只包含 en、zh，只输出一个 JSON 对象。")})
        attempt += 1


def _blank_length(english: str) -> int:
    """按英文原表达的可见字符数（不计空白）折算横线长度。"""
    length = len(re.sub(r"\s", "", english))
    return max(MIN_UNDERLINE, math.ceil(length * UNDERLINE_RATIO))


def _add_zh_blanks(text: str, mapping: dict[str, str]) -> str:
    """把每个加粗英文换成中文译文，并在后面补上带序号的默写横线。

    形如 **Crowds jammed the entrance** → **人群挤满了入口** 1.___________，
    横线长度按英文原文折算，方便学生对着中文默写英文。
    """
    number = 0

    def replace(match: re.Match) -> str:
        nonlocal number
        number += 1
        english = match.group(1)
        return (f"**{mapping[english]}** "
                f"{number}.{'_' * _blank_length(english)} ")

    return BOLD_PATTERN.sub(replace, text)


async def dictation_zh(md_path: str) -> tuple[str, str]:
    """把 md 里每个加粗英文翻译成中文并补默写横线，落盘同目录 md 与 pdf。

    :param md_path: 原始 md 路径，通常是 draft_story 生成的故事
    :return: (中文默写版 md 路径, pdf 路径)，文件名加 _dictation_zh 后缀
    """
    if not os.path.isfile(md_path):
        raise FileNotFoundError(f"文件不存在: {md_path}")

    with get_file_object(md_path, "r") as datafile:
        text = datafile.read()
    # 去重但保留出现顺序，同一个表达只请求一次翻译
    phrases = list(dict.fromkeys(BOLD_PATTERN.findall(text)))
    if not phrases:
        raise ValueError(f"md 里没有加粗英文，无法生成默写版：{md_path}")

    print(f"共 {len(phrases)} 个加粗片段，正在让模型翻译……")
    mapping = await _translate(phrases)

    base, ext = os.path.splitext(md_path)
    new_mdpath = f"{base}_dictation_zh{ext}"
    with get_file_object(new_mdpath, "w") as datafile:
        datafile.write(_add_zh_blanks(text, mapping))
    print(f"中文默写版 Markdown 已保存：{new_mdpath}")

    # md_to_pdf 是同步阻塞调用，放进线程避免卡住事件循环
    pdfpath = await asyncio.to_thread(md_to_pdf, new_mdpath)
    print(f"中文默写版 PDF 已生成：{pdfpath}")
    return new_mdpath, pdfpath
