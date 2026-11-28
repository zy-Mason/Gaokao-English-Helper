# Copyright (C) 2026 Mason 朱懿
from .prompt import jsoner
from .ai import ask_ai_notool

async def aijsoner(text):
    """返回一个字符串，为 {"items": [{"en", "zh"}, ...]} 的 JSON；结构定义见 tools/schema.py"""
    messages = [{"role": "system", "content": jsoner}, {"role": "user", "content": text}]
    answer = await ask_ai_notool(messages, response_format="json_object")
    return answer.content



