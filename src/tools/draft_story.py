# Copyright (C) 2026 Mason 朱懿
import os
from datetime import datetime

from .ai import ask_ai_notool
from .filex import get_file_object, OUTPUT_DIR
from .parse import render
from .prompt import story_maker


async def draft_story(top_items: list) -> str:
    """把打分靠前的词条交给模型写成故事，落盘为 md，返回 md 路径。

    :param top_items: 已按分数排好序并截取的词条列表，形如 [{"en":"grassy","zh":"长满草的","score":9.5}]
    :return: 生成的 md 文件路径
    """
    # 渲染成扁平文本，交给模型写故事
    text = render({"items": top_items})
    messages = [
        {"role": "system", "content": story_maker},
        {"role": "user", "content": text},
    ]
    print("正在让模型写故事……")
    answer = await ask_ai_notool(messages,reasoning_effort="max")
    # 文件名带时间戳，避免覆盖之前生成的故事
    mdpath = os.path.join(OUTPUT_DIR, f"story_{datetime.now():%Y%m%d_%H%M%S}.md")
    with get_file_object(mdpath, "w") as datafile:
        datafile.write(answer.content)
    print(f"Markdown 已保存：{mdpath}")
    return mdpath
