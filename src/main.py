# Copyright (C) 2026 Mason 朱懿
import asyncio
import glob
import os

from tools.filex import OUTPUT_DIR, md_to_pdf
from tools.process import (
    clear_scores,
    main as process_main,
    make_story,
    rank_words,
    recognize_images,
)
from tools.to_dictation import dictation, dictation_zh

MENU = """请选择要执行的流程：
  1. 识别图片为 JSON
  2. 给词条打分
  3. 写故事并转 PDF
  4. 清除 JSON 中的分数（重新打分前使用）
  5. 走完整流程（识别 → 打分 → 故事 → PDF）
  6. 生成默写版 md（加横线）并转 PDF
  7. 把指定 md 转成同目录 PDF
  8. 生成中文默写版（译文+横线）并转 PDF
  0. 退出"""


def ask_md_path() -> str | None:
    """交互读取要生成默写版的 md 路径，直接回车则取 output 里最新生成的故事 md。"""
    path = input("请输入要转换的 md 路径：").strip()
    if path:
        return path
    mds = [f for f in glob.glob(os.path.join(OUTPUT_DIR, "*.md"))
           if "_dictation" not in os.path.basename(f)]
    if not mds:
        print(f"{OUTPUT_DIR} 下没有故事 md，请先生成故事")
        return None
    latest = max(mds, key=os.path.getmtime)
    print(f"使用最新的故事 md：{latest}")
    return latest


def ask_word_num() -> int:
    """交互读取故事要用的单词数量，保证是正整数。"""
    while True:
        text = input("请输入要取出的单词数量：").strip()
        if text.isdigit() and int(text) > 0:
            return int(text)
        print("请输入一个正整数")


async def run_choice(choice: str) -> None:
    """执行用户选择的单个流程。"""
    if choice == "1":
        await recognize_images()
    elif choice == "2":
        await rank_words()
    elif choice == "3":
        mdpath = await make_story(ask_word_num())
        if mdpath:
            # md_to_pdf 是同步阻塞调用，放进线程避免卡住事件循环
            pdfpath = await asyncio.to_thread(md_to_pdf, mdpath)
            print(f"PDF 已生成：{pdfpath}")
    elif choice == "4":
        clear_scores()
    elif choice == "5":
        await process_main(ask_word_num())
    elif choice == "6":
        mdpath = ask_md_path()
        if mdpath:
            new_mdpath = dictation(mdpath)
            # md_to_pdf 是同步阻塞调用，放进线程避免卡住事件循环
            pdfpath = await asyncio.to_thread(md_to_pdf, new_mdpath)
            print(f"PDF 已生成：{pdfpath}")
    elif choice == "7":
        mdpath = input("请输入要转 PDF 的 md 路径：").strip()
        if not mdpath:
            print("未输入路径，已取消")
            return
        # PDF 与 md 同目录，文件名相同；md_to_pdf 是同步阻塞调用，放进线程
        pdfpath = await asyncio.to_thread(md_to_pdf, mdpath)
        print(f"PDF 已生成：{pdfpath}")
    elif choice == "8":
        mdpath = ask_md_path()
        if mdpath:
            # 翻译和转 PDF 都在 dictation_zh 里完成，成功后会打印两个路径
            await dictation_zh(mdpath)


def interact() -> None:
    """命令行交互：每执行完一个流程就回到菜单，直到用户选择退出。"""
    while True:
        print(MENU)
        choice = input("请输入选项编号：").strip()
        if choice == "0":
            print("已退出")
            return
        if choice not in {"1", "2", "3", "4", "5", "6", "7", "8"}:
            print("无效的选项，请重新输入")
            continue
        try:
            asyncio.run(run_choice(choice))
        except Exception as exc:  # 单个流程失败不退出，回到菜单重新选择
            print(f"执行出错：{exc}")


if __name__ == "__main__":
    interact()
