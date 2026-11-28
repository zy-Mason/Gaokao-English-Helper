# Copyright (C) 2026 Mason 朱懿
'''这是一个渲染函数，可以把json变成扁平字符串；json 结构定义见 tools/schema.py'''
from .schema import EN_KEY, ITEMS_KEY, SCORE_KEY, ZH_KEY

def render(json):
    items = json.get(ITEMS_KEY, [])
    result = ""
    for item in items:
        en = item.get(EN_KEY, "")
        zh = item.get(ZH_KEY, "")
        score = item.get(SCORE_KEY, "")
        result += f"{en} {zh} {score}\n"
    return result
