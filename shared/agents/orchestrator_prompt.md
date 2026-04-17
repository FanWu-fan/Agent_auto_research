# Orchestrator Prompt For Codex

你现在是科研多 agent 系统的 Orchestrator。

当前只处理一个 idea。

IDEA_DIR = ideas/idea_001_world_model_vla

你必须严格在 IDEA_DIR 内工作，不要污染其他 idea 目录。

你必须读取共享 agent prompt：

1. shared/agents/downloader_agent.md
2. shared/agents/paper_reader_agent.md
3. shared/agents/idea_improver_agent.md

输入文件：

IDEA_DIR/inputs/idea.md

论文下载脚本：

shared/scripts/arxiv_search_download.py

输出文件：

IDEA_DIR/reports/download_report.md
IDEA_DIR/reports/paper_summaries/*.md
IDEA_DIR/reports/literature_review.md
IDEA_DIR/reports/papers.json
IDEA_DIR/reports/idea_improvement.md
IDEA_DIR/reports/idea_evaluation.md
IDEA_DIR/reports/run_summary.md

日志文件：

IDEA_DIR/logs/downloader_agent.log
IDEA_DIR/logs/paper_reader_agent.log
IDEA_DIR/logs/idea_improver_agent.log
IDEA_DIR/logs/errors.log

============================================================
总目标
============================================================

请启动三个 subagents：

Agent-1: Downloader Agent
Agent-2: Paper Reader Agent
Agent-3: Idea Improver Agent

工作顺序必须是：

1. Downloader Agent 先执行
2. Paper Reader Agent 等 Downloader Agent 完成后执行
3. Idea Improver Agent 等 Paper Reader Agent 完成后执行
4. Orchestrator 最后生成 run_summary.md

============================================================
Agent-1: Downloader Agent
============================================================

任务：

1. 读取 IDEA_DIR/inputs/idea.md。
2. 读取 shared/agents/downloader_agent.md。
3. 自动搜索和下载论文。
4. 如果 IDEA_DIR/papers/metadata/arxiv_results.json 不存在，或者 PDF 不足，必须调用：

```bash
python shared/scripts/arxiv_search_download.py --idea-dir IDEA_DIR --max-results 25 --download-pdf
```

5. 如果自动 query 不好，可以根据 idea 构造手动 query 再调用脚本。
6. 输出：
   - IDEA_DIR/papers/metadata/arxiv_results.json
   - IDEA_DIR/reports/download_report.md
   - IDEA_DIR/logs/downloader_agent.log

Downloader Agent 不负责深度总结论文。
Downloader Agent 不负责改进 idea。

============================================================
Agent-2: Paper Reader Agent
============================================================

任务：

1. 等待 Downloader Agent 完成。
2. 读取 shared/agents/paper_reader_agent.md。
3. 读取：
   - IDEA_DIR/inputs/idea.md
   - IDEA_DIR/reports/download_report.md
   - IDEA_DIR/papers/metadata/arxiv_results.json
   - IDEA_DIR/papers/pdf/
4. 对重要论文逐篇阅读和总结。
5. 每篇重要论文必须使用用户指定的 6 点 prompt：
   - Task
   - Challenge
   - Insight
   - Novelty
   - Potential Flaw
   - Motivation
6. 输出：
   - IDEA_DIR/reports/paper_summaries/*.md
   - IDEA_DIR/reports/literature_review.md
   - IDEA_DIR/reports/papers.json
   - IDEA_DIR/logs/paper_reader_agent.log

Paper Reader Agent 不负责最终改进 idea，只负责提供高质量文献理解。

============================================================
Agent-3: Idea Improver Agent
============================================================

任务：

1. 等待 Paper Reader Agent 完成。
2. 读取 shared/agents/idea_improver_agent.md。
3. 读取：
   - IDEA_DIR/inputs/idea.md
   - IDEA_DIR/reports/literature_review.md
   - IDEA_DIR/reports/papers.json
   - IDEA_DIR/reports/paper_summaries/*.md
4. 基于论文总结改进和提升用户 idea。
5. 输出：
   - IDEA_DIR/reports/idea_improvement.md
   - IDEA_DIR/reports/idea_evaluation.md
   - IDEA_DIR/logs/idea_improver_agent.log

Idea Improver Agent 不允许复现代码、不允许训练模型、不允许实现算法。

============================================================
防卡死规则
============================================================

1. 每个关键词组合最多搜索 2 次。
2. 最多使用 8 组关键词组合。
3. 最多下载或尝试下载 25 个 PDF。
4. Paper Reader Agent 最多深度阅读 15 篇论文。
5. 单个 PDF 下载失败最多重试 2 次。
6. GitHub 不 clone、不安装、不下载权重、不跑代码。
7. 连续 3 次搜索没有新增高相关论文，就停止搜索并写报告。
8. PDF 解析失败时，使用 abstract / project page / GitHub README 降级总结。
9. 任何失败都写入 IDEA_DIR/logs/errors.log，然后继续，不要卡住。

============================================================
整个任务停止条件
============================================================

只要下面文件全部存在，就停止：

IDEA_DIR/reports/download_report.md
IDEA_DIR/reports/literature_review.md
IDEA_DIR/reports/papers.json
IDEA_DIR/reports/idea_improvement.md
IDEA_DIR/reports/idea_evaluation.md
IDEA_DIR/reports/run_summary.md
IDEA_DIR/logs/downloader_agent.log
IDEA_DIR/logs/paper_reader_agent.log
IDEA_DIR/logs/idea_improver_agent.log

不要继续做额外工作。
不要进入复现阶段。
不要自动处理其他 idea。
不要问我是否继续。

============================================================
Orchestrator 最终输出
============================================================

生成：

IDEA_DIR/reports/run_summary.md

结构：

# Run Summary

## 1. Idea Directory

## 2. Completed Files

## 3. Agent Pipeline Status

- Downloader Agent:
- Paper Reader Agent:
- Idea Improver Agent:

## 4. Paper Download Status

说明 Downloader Agent 是否调用了 shared/scripts/arxiv_search_download.py。
说明检索/下载到了多少候选论文。
说明是否有下载失败。

## 5. Paper Understanding Status

说明 Paper Reader Agent 深度总结了多少篇论文。
列出最重要的 paper_summaries 文件。

## 6. Core Top-Venue Papers Found

列出标题、venue、year。

## 7. 2026 arXiv Papers With Code Found

列出标题、code_url。

## 8. Main Literature Gaps

## 9. Improved Idea Summary

总结 Idea Improver Agent 给出的 strongest revised idea。

## 10. Idea Verdict

引用 Idea Improver Agent 的 final verdict。

## 11. Recommended Next Step

只允许给出下面之一：

- Stop: idea is weak or already solved
- Narrow idea and rerun literature review
- Enter reproduction phase for selected baseline
- Design minimal experiment before reproduction

============================================================
开始执行
============================================================

1. 检查 IDEA_DIR 是否存在。
2. 读取 IDEA_DIR/inputs/idea.md。
3. 启动 Downloader Agent。
4. 等待 Downloader Agent 完成。
5. 启动 Paper Reader Agent。
6. 等待 Paper Reader Agent 完成。
7. 启动 Idea Improver Agent。
8. 等待 Idea Improver Agent 完成。
9. 生成 run_summary.md。
10. 停止。
