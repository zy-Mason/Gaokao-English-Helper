# Copyright (C) 2026 Mason 朱懿
'''这是一个渲染函数，可以把json变成扁平字符串，json形如{"items": [{"en": "英文", "zh": "中文", "score": 8}]}'''

def render(json):
    items = json.get("items", [])
    result = ""
    for item in items:
        en = item.get("en", "")
        zh = item.get("zh", "")
        score = item.get("score", "")
        result += f"{en} {zh} {score}\n"
    return result
