# Copyright (C) 2026 Mason 朱懿
from .filex import find_images
from .dsocr import dsocr
from .word_jsoner import aijsoner
from .filex import DATA_DIR, md_to_pdf
from .schema import (
    EN_KEY,
    ITEMS_KEY,
    SCORE_KEY,
    WORD_JSON_PATH,
    ZH_KEY,
    has_score,
    load_items,
    new_item,
    save_items,
)
from .rank import rank_json
from .draft_story import draft_story
import os
import json
import asyncio

# 同时处理的图片数，避免一次性发出过多请求
IMAGE_CONCURRENCY = 50

async def process_images(picpath):
    """识别一张图片并返回新词条（WordItem 列表，见 schema.py）；不落盘，由调用方合并后统一写入。"""
    raw_word : str = await dsocr(picpath)
    json_word : str = await aijsoner(raw_word)
    # 新词条先标记为未打分（score 为 None），交给 rank.rank_json 统一打分，保持 word.json 结构一致
    json_words = [new_item(item[EN_KEY], item[ZH_KEY])
                  for item in json.loads(json_word)[ITEMS_KEY]]

    print(f"    {picpath} 识别出 {len(json_words)} 条词条")
    return json_words

def save_words(json_words: list) -> str:
    """把新词条追加进 word.json 并返回文件路径；集中写入，避免并发互相覆盖。"""
    former_words = load_items()
    return save_items(former_words + json_words)

async def recognize_images(path: str | None = None) -> str | None:
    """识别 path 目录下的图片，把新词条（未打分）追加进 word.json，返回 json 路径。

    path 为空时交互询问，直接回车则使用默认图片目录；
    没有识别到任何词条时返回 None。
    """
    if not path:
        path = input("请输入图片路径")
        if not path:
            path = os.path.join(DATA_DIR, "images")
            print(f"使用默认路径：{path}")
    if not os.path.exists(path):
        print("路径不存在，请检查后重试")
        return None

    piclist = find_images(path)
    total = len(piclist)
    if not total:
        print(f"目录里没有图片：{path}")
        return None
    semaphore = asyncio.Semaphore(IMAGE_CONCURRENCY)

    async def recognize(index, picpath):
        async with semaphore:
            print(f"[{index}/{total}] 正在识别图片：{picpath}")
            return await process_images(picpath)

    # 多张图片并发识别，全部识别完再一次性写库
    # all_words 是一个列表的列表，每个内层列表是一张图片识别出的 WordItem（见 schema.py）
    all_words = await asyncio.gather(*(recognize(index, picpath)
                                      for index, picpath in enumerate(piclist, 1)))
    print("所有图片识别完成，开始写入词条……")
    json_words = [word for words in all_words for word in words]
    if not json_words:
        print("没有识别出任何词条，未写入 word.json")
        return None
    jsonpath = save_words(json_words)
    print(f"词条已写入：{jsonpath}")
    return jsonpath

async def rank_words() -> list:
    """给 word.json 中未打分的词条打分并写回，返回全部词条。"""
    print("开始给词条打分……")
    return await rank_json()

async def make_story(word_num: int) -> str | None:
    """取分数最高的 word_num 个词条生成故事，返回 md 路径；不负责转 PDF。

    词条来自 word.json，还没有分数时会顺带补打分。
    """
    items = await rank_json()
    # 取分数最高的 word_num 个词条，没有分数的按 0 处理
    top_items = sorted(items, key=lambda item: item.get(SCORE_KEY) or 0, reverse=True)[:word_num]
    if not top_items:
        print("word.json 里没有可用的词条，请先识别图片再生成故事")
        return None
    print(f"共 {len(items)} 个词条，取分数最高的 {len(top_items)} 个生成故事")
    return await draft_story(top_items)

def clear_scores(jsonpath: str | None = None) -> int:
    """把 json 中所有词条的分数置为 None，供重新打分；返回被清除的分数个数。"""
    if jsonpath is None:
        jsonpath = WORD_JSON_PATH
    items = load_items(jsonpath)
    if not items:
        print("json 文件为空，没有需要清除的分数")
        return 0
    cleared = 0
    for item in items:
        if has_score(item):
            cleared += 1
        item[SCORE_KEY] = None
    save_items(items, jsonpath)
    print(f"已清除 {cleared} 个词条的分数，写回：{jsonpath}")
    return cleared

async def main(word_num : int):
    """完整流程：识别图片 → 打分 → 写故事 → 转 PDF。"""
    if not await recognize_images():
        return
    await rank_words()
    mdpath = await make_story(word_num)
    if not mdpath:
        return
    # md_to_pdf 是同步阻塞调用，放进线程避免卡住事件循环
    pdfpath = await asyncio.to_thread(md_to_pdf, mdpath)
    print(f"PDF 已生成：{pdfpath}")






