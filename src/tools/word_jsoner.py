# Copyright (C) 2026 Mason 朱懿
from .prompt import jsoner
from .ai import ask_ai_notool

async def aijsoner(text):
    """返回一个字符串，形如{"items":[{"en":"grassy","zh":"长满草的"},{"en":"grassland","zh":"草地"}]}"""
    messages = [{"role": "system", "content": jsoner}, {"role": "user", "content": text}]
    answer = await ask_ai_notool(messages, response_format="json_object")
    return answer.content



