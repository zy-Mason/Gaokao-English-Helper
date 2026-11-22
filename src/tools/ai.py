# Copyright (C) 2026 Mason 朱懿
import asyncio
import base64
import os

from openai import AsyncOpenAI

_client = None
_client_loop = None


def _get_client() -> AsyncOpenAI:
    """复用同一个客户端，避免每次请求都重建连接池；事件循环变了就重建。"""
    global _client, _client_loop
    loop = asyncio.get_running_loop()
    if _client is None or _client_loop is not loop:
        _client = AsyncOpenAI(
            api_key=os.getenv('DEEPSEEK_API_KEY'),
            base_url="https://api.deepseek.com/",
        )
        _client_loop = loop
    return _client


# noinspection bad-argument-type
async def ask_ai_notool(messages: list,
                 reasoning_effort: str = "high",
                 response_format: str = "text"):
    """返回一个message,使用.content,.reasoning_content获得内容。记得在协程里面await"""
    client = _get_client()
    response = await client.chat.completions.create(
        model="deepseek-flash",
        messages=messages,
        stream=False,
        reasoning_effort=reasoning_effort,
        extra_body={"thinking": {"type": "enabled"}},
        response_format={"type": response_format},
        max_tokens=100000,
        tool_choice="none",)
    return response.choices[0].message


def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")




