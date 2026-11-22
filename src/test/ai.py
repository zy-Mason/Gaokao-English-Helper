# Copyright (C) 2026 Mason 朱懿
from tools.ai import ask_ai_notool
import asyncio


def test_ask_ai_notool():
    async def main():
        messages = [{"role": "user", "content": "Hello, how are you?"}]
        a = await ask_ai_notool(messages,reasoning_effort="low")
        print(a.content)

    asyncio.run(main())
