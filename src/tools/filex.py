# Copyright (C) 2026 Mason 朱懿
import os
from pathlib import Path
import pdfpecker

OUTPUT_DIR = "output"
DATA_DIR = "data"

def get_file_object(file_path: str,
                    mode: str="w+",
                    encoding: str="utf-8"
                    ):
    """
    传入一个文件路径字符串。
    如果路径不存在，则创建对应的目录和空文件。
    最后返回一个打开的文件对象（读写模式，指针在开头）。
    """
    # 获取文件所在目录
    directory = os.path.dirname(file_path)
    # 如果目录非空且不存在，则递归创建目录
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

    # 如果文件不存在，则创建一个空文件
    if not os.path.exists(file_path):
        # 使用 'w' 模式创建空文件后立即关闭
        with open(file_path, 'w', encoding=encoding):
            pass

    # 以读写模式打开文件（文件已存在，不会清空内容，指针在开头）
    return open(file_path, mode, encoding=encoding)


def find_images(path):
    """返回 path 目录下一层的所有图片文件路径（不递归）

    :param path: 目录路径
    :return: 图片路径列表（字符串）
    """
    IMG_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".tif", ".tiff", ".svg", ".ico", ".heic", ".avif"}

    p = Path(path)
    if not p.is_dir():
        raise NotADirectoryError(f"不是有效目录: {path}")

    return [
        str(f)
        for f in p.iterdir()
        if f.is_file() and f.suffix.lower() in IMG_EXTS
    ]






def md_to_pdf(md_path: str) -> str:
    """将 md 文件转换为 pdf，返回 pdf 路径"""

    # 按 Linux → Windows → macOS 顺序回退；找不到会自动跳过下一个，
    # 英文族名 + 中文别名都列，提高各系统字体枚举命中率。
    # 如需再补，可加 "Source Han Sans SC","DengXian","SimSun","宋体",
    # "Arial Unicode MS" 等标准族名，未命中不会报错。
    CJK_STYLE_SHEET = """
    * { font-family: "Noto Sans CJK SC", "Microsoft YaHei", "微软雅黑",
                    "PingFang SC", "苹方-简", "Hiragino Sans GB", "Heiti SC",
                    "WenQuanYi Micro Hei", "SimHei", sans-serif; }
    code, pre, pre *, code *, tt, kbd, samp {
      font-family: "Noto Sans CJK SC", "Microsoft YaHei", "微软雅黑",
                   "PingFang SC", "苹方-简", "Hiragino Sans GB", "Heiti SC",
                   "WenQuanYi Micro Hei", "SimHei", monospace !important;
    }
    """
    if not os.path.isfile(md_path):
        raise FileNotFoundError(f"文件不存在: {md_path}")

    md_path = os.path.abspath(md_path)
    base, _ = os.path.splitext(md_path)
    pdf_path = base + ".pdf"

    pdfpecker.markdown_file_to_pdf(
        md_path,
        pdf_path,
        use_system_fonts=True,              # 允许按 font-family 查系统字体
        user_style_sheet=CJK_STYLE_SHEET,  # 正文与 code/pre 用同一套字体栈
    )
    return pdf_path