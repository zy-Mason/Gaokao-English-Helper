# Copyright (C) 2026 Mason 朱懿
"""词条数据结构与 JSON 契约的唯一定义点。

词条（WordItem）形如 {"en": "英文", "zh": "中文", "score": 8.5 | None}，
词条库文件形如 {"items": [WordItem, ...]}。
键名、默认路径、读写与模型返回的容错解析都集中在这里；
prompt.py 中提示词文本的 JSON 格式说明须与此处人工同步。
"""
import json
import os
from typing import TypedDict

from .filex import DATA_DIR, get_file_object

ITEMS_KEY = "items"
EN_KEY = "en"
ZH_KEY = "zh"
SCORE_KEY = "score"

# 词条库的默认路径
WORD_JSON_PATH = os.path.join(DATA_DIR, "json", "word.json")


class WordItem(TypedDict):
    """一条词条：en 英文，zh 中文，score 重要性分数（None 表示未打分）。"""
    en: str
    zh: str
    score: float | None


def new_item(en: str, zh: str) -> WordItem:
    """创建一条新词条，初始为未打分（score 为 None）。"""
    return {EN_KEY: en, ZH_KEY: zh, SCORE_KEY: None}


def has_score(item: dict) -> bool:
    """判断词条是否已有合法分数；rank 的跳过逻辑与 clear 的统计逻辑共用，保证语义一致。"""
    return isinstance(item.get(SCORE_KEY), (int, float))


def load_items(path: str = WORD_JSON_PATH) -> list:
    """读取词条库文件并返回词条列表；文件为空时视为还没有任何词条。"""
    with get_file_object(path, "r") as datafile:
        text = datafile.read()
    if not text.strip():
        return []
    return json.loads(text)[ITEMS_KEY]


def save_items(items: list, path: str = WORD_JSON_PATH) -> str:
    """把词条列表整体写回词条库文件，返回文件路径。"""
    with get_file_object(path, "w") as datafile:
        json.dump({ITEMS_KEY: items}, datafile, ensure_ascii=False, indent=4)
    return path


def loads_object(text: str) -> dict:
    """容错解析模型返回：忽略代码围栏等前后缀，截取最外层 JSON 对象。"""
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end <= start:
        raise ValueError(f"模型没有返回 JSON 对象：{text[:200]}")
    return json.loads(text[start:end + 1])
