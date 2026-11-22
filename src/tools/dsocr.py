# Copyright (C) 2026 Mason 朱懿
import asyncio

from .ai import ask_ai_notool, image_to_base64
from .prompt import ocrer

async def dsocr(image_path):
    """传入一个图片路径，返回图片中的文字。记得await"""
    # 读图是同步 IO，放线程里避免阻塞事件循环
    b64 = await asyncio.to_thread(image_to_base64, image_path)
    messages = [
        {"role": "system", "content": ocrer},
        {"role": "user",
        "content": [
            {"type": "text", "text": "这张图片里有什么？"},
            {"type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{b64}"},
            },
        ],
        }
    ]
    answer =await ask_ai_notool(messages)
    return answer.content



