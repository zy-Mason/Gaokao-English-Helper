# 高考英语单词助手（Gaokao-English-Helper）

## 这是什么

一个面向**高考英语备考**的本地小工具：把你在笔记本上抄的单词笔记拍成照片，自动识别、整理成词条库，按"高考重要性"打分，再挑出高分词条让大模型写成一篇地道英语小故事，并输出 Markdown / PDF。此外还提供两种"默写版"导出，方便背完就测。

完整链路：

```
笔记照片 → OCR 识别 → 结构化词条(JSON) → 重要性打分 → AI 写故事(md/pdf)
                                              ├→ 默写版（加横线）
                                              └→ 中文默写版（译文+横线）
```

核心特点：

- **全自动流水线**：一次可并发识别几十张图片，OCR、拆词、打分、写作全程由大模型完成。
- **打分有据可依**：按"高三学生已掌握 3500 词"的基线，结合短语优先、熟词生义加分等规则打分，多轮随机分组取平均，拉开分差。
- **故事带动记忆**：200–350 词的连贯小故事，目标词以加粗嵌入语境，符合读后续写/应用文的表达习惯。
- **配套默写练习**：在故事基础上自动生成横线填空版（保留英文）和中文提示版（写出英文），一键转 PDF。

## 项目结构

```
src/
├── main.py               # 命令行入口，交互菜单
├── requirements.txt      # 第三方依赖
├── tools/
│   ├── ai.py             # 大模型调用封装（openai SDK + DeepSeek）
│   ├── prompt.py         # 提示词库（拆词、打分、写故事、翻译、OCR）
│   ├── dsocr.py          # 图片 OCR（视觉模型）
│   ├── word_jsoner.py    # 笔记原文 → 结构化词条
│   ├── rank.py           # 词条重要性打分
│   ├── draft_story.py    # 生成英语故事并落盘 md
│   ├── to_dictation.py   # 默写版（横线 / 中文译文）生成
│   ├── filex.py          # 文件读写、图片查找、md → pdf
│   ├── parse.py          # 词条渲染成扁平文本
│   └── process.py        # 主流程编排
├── data/
│   ├── images/           # 待识别的笔记照片
│   └── json/word.json    # 词条库（自动生成）
├── output/               # 生成的故事 md/pdf（不入库）
└── test/                 # 临时脚本
```

## 怎么使用

### 1. 环境要求

- Python 3.10+
- 可用的 DeepSeek API Key（模型 `deepseek-flash`）
- 系统装有中文字体（如微软雅黑），否则转 PDF 时中文可能显示异常

### 2. 安装依赖

```powershell
pip install -r src/requirements.txt
```

依赖只有两个：`openai`（调用模型）和 `pdfpecker`（Markdown 转 PDF）。

### 3. 配置 API Key

通过环境变量提供，代码中读取 `DEEPSEEK_API_KEY`：

```powershell
$env:DEEPSEEK_API_KEY = "sk-xxxx"
```

在 PyCharm 里运行的话，也可以写到 Run Configuration 的环境变量中。

### 4. 运行

```powershell
cd src
python main.py
```

按菜单选择流程：

| 选项 | 功能 | 说明 |
| --- | --- | --- |
| 1 | 识别图片为 JSON | 识别 `data/images/`（或手动输入的目录）下的笔记照片，词条追加进 `data/json/word.json` |
| 2 | 给词条打分 | 只给未打分的词条打分，已打分的跳过 |
| 3 | 写故事并转 PDF | 输入取词数量，取分数最高的若干个词写故事，输出 `output/story_时间戳.md` 和同名 PDF |
| 4 | 清除分数 | 把所有词条分数置空，便于整体重新打分 |
| 5 | 完整流程 | 识别 → 打分 → 故事 → PDF 一次走完 |
| 6 | 默写版 | 选一个故事 md（回车默认取 `output` 下最新的），在每个加粗英文后补编号横线，输出 `_dictation.md` + PDF |
| 7 | 指定 md 转 PDF | 输入任意 md 路径，在同目录生成同名 PDF |
| 8 | 中文默写版 | 用大模型把加粗英文译成中文，替换后补横线，输出 `_dictation_zh.md` + PDF |
| 0 | 退出 | |

### 5. 数据与输出

- 笔记照片放 `src/data/images/`，支持 jpg/png/webp 等常见格式（不递归子目录）。
- 词条库 `src/data/json/word.json`，结构为 `{"items": [{"en": "英文", "zh": "中文", "score": 8.5}]}`。
- 所有生成结果落在 `src/output/`：故事带时间戳不会覆盖；默写版按原文件名加后缀，重复生成会覆盖同名文件。
- `data/`、`output/`、`.idea/`、`__pycache__/` 已在 `.gitignore` 中忽略。

### 6. 生成效果示例

故事 md：

```markdown
Critics said she liked to **run the company with an iron fist**, and she never **bother to deny** it.
```

默写版（选项 6）：

```markdown
Critics said she liked to **run the company with an iron fist** 1.________________, and she never **bother to deny** 2.______ it.
```

中文默写版（选项 8）：

```markdown
Critics said she liked to **铁腕管理公司** 1.______________, and she never **费心否认** 2.______ it.
```

## Q&A

**Q1：运行时报错提示没有 API Key / 401？**
检查 `DEEPSEEK_API_KEY` 是否已设置且在启动进程的同一终端里生效。改完环境变量后需要重启终端或 Run Configuration。

**Q2：转出来的 PDF 中文是方块或乱码？**
`md_to_pdf` 会按字体栈查找系统中文字体（微软雅黑、宋体等），请确认系统已安装中文字体；也可以在 `tools/filex.py` 的 `CJK_STYLE_SHEET` 里补充字体名。

**Q3：打分要花很久吗？会不会重复花钱？**
只对未打分的词条发起请求，已打分的直接跳过。如需整体重打，先选 4 清除分数。打分默认 3 轮随机分组取平均，比单轮更稳，但请求量也约为 3 倍。

**Q4：模型返回的条数和输入对不上怎么办？**
打分与翻译都有容错：会把不合格回答接回对话并要求重发，最多 3 次（`rank.py` / `to_dictation.py` 中的 `MAX_ATTEMPTS`），仍失败才报错，不会污染词条库。

**Q5：故事太长/太短、词语用得太少？**
故事长度和用词规则由 `tools/prompt.py` 的 `story_maker` 控制，可以在里面调整字数范围和"尽量多用词条"的要求；选项 3/5 输入的取词数量决定喂给模型的词条上限。

**Q6：默写横线为什么有的长有的短？**
横线长度 = 加粗部分可见字符数（不计空格）× 0.5，最少 4 个下划线，让你大致能看出要默写的表达有多长。想整体调长/调短，改 `to_dictation.py` 里的 `UNDERLINE_RATIO`。

**Q7：中文默写版用的是哪个模型的翻译？**
同一套 DeepSeek 模型，由 `prompt.py` 中的 `translator` 提示词约束：译文要能反向提示出英文原表达，不扩写成解释；返回条数与输入不一致时会自动要求重发。

**Q8：可以识别手写笔记吗？**
OCR 提示词要求忽略手写内容、只识别印刷文字。手写笔记建议先誊写或用其他方式数字化后再录入。

**Q9：图片一次放太多会被限流吗？**
识别和打分都有并发控制（`process.py` 的 `IMAGE_CONCURRENCY`、`rank.py` 的 `MAX_CONCURRENCY`），如果仍遇到接口限流，把这两个值调小即可。

## 许可

本项目采用 **GNU Affero General Public License v3.0（AGPL-3.0）** 发布，完整条款见仓库根目录的 [LICENSE](../LICENSE) 文件。

Copyright (C) 2026 Mason 朱懿

简单提醒：

- 可以自由使用、修改、分发本项目的代码，但衍生作品需同样以 AGPL-3.0 开源，并保留版权声明。
- AGPL 的关键要求：**即使只通过网络提供服务**（例如部署成在线服务），也必须向使用者提供对应的完整源码。
- 本项目调用的第三方模型 API（DeepSeek 等）及生成内容的合规性，需自行遵守相应服务条款。
