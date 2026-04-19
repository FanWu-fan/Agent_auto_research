# Agent Auto Research

English | 中文
--- | ---
A multi-agent workflow for early-stage research idea exploration. | 一个面向科研 idea 前期调研的多 Agent 工作流项目。
Core pipeline: `Downloader Agent -> Paper Reader Agent -> Idea Improver Agent` | 核心流水线：`Downloader Agent -> Paper Reader Agent -> Idea Improver Agent`

## 1. Project Goal / 项目目标

**English**

This repository helps you turn an initial research idea into a structured literature review and a theory-level idea assessment.
At the current stage, the system focuses on:

- paper search and download
- paper reading and summarization
- literature review construction
- idea refinement and evaluation

It does **not** focus on:

- code reproduction
- model training
- algorithm implementation
- large-scale experiments
- cloning large repositories
- downloading model weights

**中文**

这个仓库用于把一个原始科研想法逐步整理成结构化的文献综述和理论层面的 idea 评估。
当前阶段重点是：

- 论文搜索与下载
- 论文阅读与总结
- 文献综述构建
- idea 改进与评估

当前阶段**不做**：

- 代码复现
- 模型训练
- 算法实现
- 大规模实验
- clone 大仓库
- 下载模型权重

---

## 2. Directory Structure / 目录结构

```text
~/Agent_auto_research/
├── requirements.txt
├── README.md
├── ideas/
│   ├── idea_001_xxx/
│   │   ├── inputs/
│   │   │   └── idea.md
│   │   ├── papers/
│   │   │   ├── pdf/
│   │   │   └── metadata/
│   │   ├── reports/
│   │   │   ├── paper_summaries/
│   │   │   │   ├── 01_xxx.md
│   │   │   │   └── 02_xxx.md
│   │   │   ├── download_report.md
│   │   │   ├── literature_review.md
│   │   │   ├── papers.json
│   │   │   ├── idea_improvement.md
│   │   │   ├── idea_evaluation.md
│   │   │   └── run_summary.md
│   │   └── logs/
│   │       ├── downloader_agent.log
│   │       ├── paper_reader_agent.log
│   │       ├── idea_improver_agent.log
│   │       └── errors.log
│   └── ...
└── shared/
    ├── agents/
    │   ├── downloader_agent.md
    │   ├── paper_reader_agent.md
    │   ├── idea_improver_agent.md
    │   └── orchestrator_prompt.md
    ├── scripts/
    │   ├── create_idea.sh
    │   └── arxiv_search_download.py
    └── templates/
        └── idea_template.md
```

---

## 3. Installation / 安装

```bash
cd ~/Agent_auto_research
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
chmod +x shared/scripts/create_idea.sh
chmod +x shared/scripts/arxiv_search_download.py
```

**English**

Create a virtual environment first so your research workflow stays isolated.

**中文**

建议优先使用虚拟环境，避免污染系统 Python 环境。

---

## 4. Create a New Idea / 创建新的 idea

```bash
bash shared/scripts/create_idea.sh idea_001_world_model_vla
```

This creates / 它会创建：

```text
ideas/idea_001_world_model_vla/
├── inputs/idea.md
├── papers/pdf/
├── papers/metadata/
├── reports/paper_summaries/
├── reports/
└── logs/
```

---

## 5. Fill in the Idea File / 填写 idea 文件

```bash
nano ideas/idea_001_world_model_vla/inputs/idea.md
```

Recommended minimum fields / 最少建议填写：

- Problem
- Observation
- Core Insight
- Proposed Method
- Target Domain
- Expected Contribution
- Keywords
- Excluded Directions

The more specific the idea is, the less likely the agents are to drift.
写得越具体，Agent 越不容易跑偏。

---

## 6. Run Codex with Three Agents / 启动 Codex 的三 Agent 流程

```bash
cd ~/Agent_auto_research
codex
cat shared/agents/orchestrator_prompt.md
```

Paste the orchestrator prompt into Codex.
把总控 prompt 粘贴给 Codex。

Before each run, update:
每次运行前，请修改：

```text
IDEA_DIR = ideas/idea_001_world_model_vla
```

---

## 7. Agent Handoff / Agent 交接关系

### Downloader Agent

**Input / 输入**

```text
IDEA_DIR/inputs/idea.md
```

**Output / 输出**

```text
IDEA_DIR/papers/metadata/arxiv_results.json
IDEA_DIR/papers/pdf/*.pdf
IDEA_DIR/reports/download_report.md
IDEA_DIR/logs/downloader_agent.log
```

**Responsibility / 职责**

- Search for papers / 搜索论文
- Download PDFs / 下载 PDF
- Record candidates / 记录候选论文
- Do not deeply summarize / 不做深度总结
- Do not improve the idea / 不改进 idea

### Paper Reader Agent

**Input / 输入**

```text
IDEA_DIR/inputs/idea.md
IDEA_DIR/reports/download_report.md
IDEA_DIR/papers/metadata/arxiv_results.json
IDEA_DIR/papers/pdf/*.pdf
```

**Output / 输出**

```text
IDEA_DIR/reports/paper_summaries/*.md
IDEA_DIR/reports/literature_review.md
IDEA_DIR/reports/papers.json
IDEA_DIR/logs/paper_reader_agent.log
```

**Responsibility / 职责**

- Read important papers / 阅读重要论文
- Summarize with the six-part first-principles rubric / 使用六点第一性原理结构总结
- Produce literature understanding / 产出高质量文献理解

### Idea Improver Agent

**Input / 输入**

```text
IDEA_DIR/inputs/idea.md
IDEA_DIR/reports/paper_summaries/*.md
IDEA_DIR/reports/literature_review.md
IDEA_DIR/reports/papers.json
```

**Output / 输出**

```text
IDEA_DIR/reports/idea_improvement.md
IDEA_DIR/reports/idea_evaluation.md
IDEA_DIR/logs/idea_improver_agent.log
```

**Responsibility / 职责**

- Improve and sharpen the idea / 改进并收敛 idea
- Evaluate novelty, baselines, risks, and experiment design / 评估创新性、baseline、风险与实验设计
- Do not reproduce or implement / 不做复现和实现

---

## 8. Six-Part Reading Rubric / 六点论文阅读框架

Paper Reader Agent should summarize important papers with the following structure:
Paper Reader Agent 需要按以下结构总结重要论文：

1. Task / 任务
2. Challenge / 挑战
3. Insight / 核心洞察
4. Novelty / 创新点
5. Potential Flaw / 潜在局限
6. Motivation / 灵感迁移方式

---

## 9. Standard Workflow / 标准完整流程

```bash
cd ~/Agent_auto_research
pip install -r requirements.txt
bash shared/scripts/create_idea.sh idea_001_world_model_vla
nano ideas/idea_001_world_model_vla/inputs/idea.md
codex
# paste shared/agents/orchestrator_prompt.md into Codex
```

After that, the pipeline should proceed as:
之后流程应为：

```text
Downloader Agent -> Paper Reader Agent -> Idea Improver Agent
```

---

## 10. Output Check / 输出检查

```bash
ls ideas/idea_001_world_model_vla/reports
ls ideas/idea_001_world_model_vla/reports/paper_summaries
cat ideas/idea_001_world_model_vla/reports/run_summary.md
less ideas/idea_001_world_model_vla/reports/idea_improvement.md
less ideas/idea_001_world_model_vla/reports/idea_evaluation.md
less ideas/idea_001_world_model_vla/reports/literature_review.md
python -m json.tool ideas/idea_001_world_model_vla/reports/papers.json | less
```

Expected key files / 关键输出文件：

- `download_report.md`
- `literature_review.md`
- `papers.json`
- `idea_improvement.md`
- `idea_evaluation.md`
- `run_summary.md`

---

## 11. Multi-Idea Management / 多 idea 管理

```bash
bash shared/scripts/create_idea.sh idea_001_world_model_vla
bash shared/scripts/create_idea.sh idea_002_semantic_slam_nav
bash shared/scripts/create_idea.sh idea_003_memory_agent
```

Only run one idea at a time.
每次只跑一个 idea。

```text
IDEA_DIR = ideas/idea_001_world_model_vla
```

---

## 12. If Codex Gets Stuck / 如果 Codex 卡住

### Downloader Agent keeps searching / Downloader Agent 一直搜索

```text
Stop searching and generate download_report.md based on the current results.
停止继续搜索，请基于目前结果立即生成 download_report.md。
```

### Downloader Agent keeps downloading PDFs / Downloader Agent 一直下载 PDF

```text
Do not continue downloading PDFs. Record failures in errors.log and generate download_report.md.
不要继续下载 PDF，把失败记录到 errors.log，然后生成 download_report.md。
```

### Paper Reader Agent keeps reading too many papers / Paper Reader Agent 读太多论文

```text
Read at most 15 papers deeply. Generate paper_summaries, literature_review.md, and papers.json now.
最多深读 15 篇论文，请立即生成 paper_summaries、literature_review.md 和 papers.json。
```

### Idea Improver Agent wants to search more papers / Idea Improver Agent 又想继续搜论文

```text
Do not launch another large-scale literature search. Finish idea_improvement.md and idea_evaluation.md from the existing summaries.
不要重新做大规模文献搜索，请基于现有总结完成 idea_improvement.md 和 idea_evaluation.md。
```

### The system tries to enter reproduction / 系统想进入复现阶段

```text
Reproduction is forbidden at the current stage. Only generate run_summary.md and stop.
当前阶段禁止复现。只生成 run_summary.md，然后停止。
```

---

## 13. Stop Condition / 停止条件

The run should stop when all of the following exist:
当以下文件全部存在时，任务应停止：

```text
IDEA_DIR/reports/download_report.md
IDEA_DIR/reports/literature_review.md
IDEA_DIR/reports/papers.json
IDEA_DIR/reports/idea_improvement.md
IDEA_DIR/reports/idea_evaluation.md
IDEA_DIR/reports/run_summary.md
IDEA_DIR/logs/downloader_agent.log
IDEA_DIR/logs/paper_reader_agent.log
IDEA_DIR/logs/idea_improver_agent.log
```

---

## 14. Suggested Next Step / 后续建议

After the current stage, read:
当前阶段结束后，请阅读：

```text
reports/run_summary.md
reports/idea_improvement.md
reports/idea_evaluation.md
```

If the verdict is:
如果 verdict 是：

- `Strong idea`
- `Promising but needs narrowing`

then you can consider entering the reproduction stage.
则可以考虑进入复现阶段。

If the verdict is:
如果 verdict 是：

- `Incremental`
- `Weak / already solved`
- `Not enough evidence`

then refine the idea or rerun the literature review first.
则建议先修改 idea 或重新做一轮 literature review。
