# Agent Auto Research

`Agent_auto_research` is a multi-agent workflow project for early-stage research idea exploration.  
`Agent_auto_research` 是一个用于科研 idea 前期调研的多 agent 工作流项目。

Core pipeline / 核心流水线：

```text
Downloader Agent -> Paper Reader Agent -> Idea Improver Agent
```

Meaning / 含义：

1. **Downloader Agent**: Automatically searches for and downloads papers based on the idea.  
   **Downloader Agent**：根据 idea 自动搜索和下载论文。

2. **Paper Reader Agent**: Reads papers one by one and summarizes them using the 6-point first-principles prompt.  
   **Paper Reader Agent**：逐篇阅读论文，并按 6 点第一性原理 prompt 总结。

3. **Idea Improver Agent**: Reads paper summaries, then improves, refines, and evaluates the user's research idea.  
   **Idea Improver Agent**：读取论文总结，改进、提升和评估用户的科研 idea。

Core principle / 核心原则：

**The human only writes the idea and launches Codex; paper search, download, interpretation, summarization, idea improvement, and theoretical evaluation are all handled by agents.**  
**人只负责写 idea 和启动 Codex；论文搜索、下载、解读、总结、idea 改进和理论评估都由 agent 完成。**

What is NOT included at the current stage / 当前阶段不做：

- Code reproduction / 代码复现
- Model training / 模型训练
- Algorithm implementation / 算法实现
- Large-scale experiments / 大规模实验
- Cloning large repositories / clone 大仓库
- Downloading model weights / 下载模型权重

---

## 1. Directory Structure / 目录结构

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

## 2. Install Dependencies / 安装依赖

Enter the project directory / 进入项目目录：

```bash
cd ~/Agent_auto_research
```

It is recommended to use a virtual environment / 建议使用虚拟环境：

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies / 安装依赖：

```bash
pip install -r requirements.txt
```

Grant execution permission to the scripts / 给脚本执行权限：

```bash
chmod +x shared/scripts/create_idea.sh
chmod +x shared/scripts/arxiv_search_download.py
```

---

## 3. Create a New Idea / 创建新的 idea

```bash
bash shared/scripts/create_idea.sh idea_001_world_model_vla
```

It will create / 它会创建：

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

## 4. Fill in the Idea / 填写 idea

Edit / 编辑：

```bash
nano ideas/idea_001_world_model_vla/inputs/idea.md
```

At minimum, fill in / 至少填写：

- Problem
- Observation
- Core Insight
- Proposed Method
- Target Domain
- Expected Contribution
- Keywords
- Excluded Directions

The more specific the idea is, the less likely the agent will drift away from the target.  
写得越具体，agent 越不容易跑偏。

---

## 5. Launch Codex and Let the Three Agents Complete the Task / 启动 Codex，由三个 agent 自动完成任务

At the project root / 在项目根目录：

```bash
cd ~/Agent_auto_research
codex
```

Copy the orchestrator prompt / 复制总控 prompt：

```bash
cat shared/agents/orchestrator_prompt.md
```

Paste the content into Codex / 把内容粘贴给 Codex。

Before each run, you only need to modify this line in the prompt / 每次运行前，只需要修改 prompt 中这一行：

```text
IDEA_DIR = ideas/idea_001_world_model_vla
```

Replace it with the current idea directory / 换成当前 idea 目录。

---

## 6. How the Three Agents Handoff / 三个 agent 如何交接

### 6.1 Downloader Agent

Input / 输入：

```text
IDEA_DIR/inputs/idea.md
```

Output / 输出：

```text
IDEA_DIR/papers/metadata/arxiv_results.json
IDEA_DIR/papers/pdf/*.pdf
IDEA_DIR/reports/download_report.md
IDEA_DIR/logs/downloader_agent.log
```

Responsibility / 作用：

```text
Only responsible for finding papers, downloading papers, and recording candidate papers.
Not responsible for deep summarization.
Not responsible for improving the idea.
```

```text
只负责找论文、下载论文、记录候选论文。
不负责深度总结。
不负责改进 idea。
```

### 6.2 Paper Reader Agent

Input / 输入：

```text
IDEA_DIR/inputs/idea.md
IDEA_DIR/reports/download_report.md
IDEA_DIR/papers/metadata/arxiv_results.json
IDEA_DIR/papers/pdf/*.pdf
```

Output / 输出：

```text
IDEA_DIR/reports/paper_summaries/*.md
IDEA_DIR/reports/literature_review.md
IDEA_DIR/reports/papers.json
IDEA_DIR/logs/paper_reader_agent.log
```

Responsibility / 作用：

```text
Summarize papers one by one with the 6-point first-principles prompt.
Pass the understanding results of the papers to the Idea Improver Agent.
```

```text
按 6 点第一性原理 prompt 逐篇总结论文。
把论文理解结果交给 Idea Improver Agent。
```

### 6.3 Idea Improver Agent

Input / 输入：

```text
IDEA_DIR/inputs/idea.md
IDEA_DIR/reports/paper_summaries/*.md
IDEA_DIR/reports/literature_review.md
IDEA_DIR/reports/papers.json
```

Output / 输出：

```text
IDEA_DIR/reports/idea_improvement.md
IDEA_DIR/reports/idea_evaluation.md
IDEA_DIR/logs/idea_improver_agent.log
```

Responsibility / 作用：

```text
Read paper summaries, improve and refine the idea.
Judge novelty, baselines, risks, experiment design, and whether it is worth continuing.
```

```text
读取论文总结，改进和提升 idea。
判断 novelty、baseline、风险、实验设计和是否值得继续。
```

---

## 7. The 6-Point Paper Interpretation Prompt Used by Paper Reader Agent / Paper Reader Agent 使用的 6 点论文解读 Prompt

The Paper Reader Agent uses the following structure for important papers / Paper Reader Agent 会对重要论文使用如下结构：

```text
1. Task
What problem does this paper solve? Please formalize it as much as possible.
这篇文章解决的是什么问题？请尽可能形式化。

2. Challenge
What challenges do traditional methods face when solving this problem?
传统的方法在解决这个问题时遇到了什么挑战？

3. Insight
What inspiration led to the authors' Insight?
作者的 Insight 是被什么 Inspiration 启发的？

4. Novelty
Where is the Novelty of this paper?
For each Novelty, describe it in this format:
[What problem does the innovation solve] -> [Which insight inspired it] -> [What innovation was designed, describe as specifically as possible]
作者本篇文章的 Novelty 体现在何处？
对于每一个 Novelty，按这个格式描述：
【创新点解决的问题是什么】 -> 【受哪个 insight 启发】 -> 【设计了什么创新点，尽可能具体描述】

5. Potential Flaw
Does the current setting have limitations?
Is it possible to extend the architecture to solve new settings, such as problems with more dimensions, more conditions, or more constraints?
当前问题的情境是否有局限？
有没有可能通过延伸架构，解决一些新情境，例如维度更多、条件更多、约束更多下的问题？

6. Motivation
Summarize the way this paper inspires a general idea, preferably in the form of a question:
Previous methods ..., so could we try xxx?
总结这篇文章想到 general idea 的方式，最好以问句形式给出：
之前的方法 ...，那可不可以尝试一下 xxx？
```

---

## 8. Normal Full Workflow / 正常完整流程

```bash
cd ~/Agent_auto_research

# 1. Install dependencies / 安装依赖
pip install -r requirements.txt

# 2. Create idea / 创建 idea
bash shared/scripts/create_idea.sh idea_001_world_model_vla

# 3. Edit idea / 编辑 idea
nano ideas/idea_001_world_model_vla/inputs/idea.md

# 4. Launch Codex / 启动 Codex
codex

# 5. Paste the prompt in shared/agents/orchestrator_prompt.md
#    粘贴 shared/agents/orchestrator_prompt.md 中的 prompt
```

After that, the agents will execute automatically / 之后由 agent 自动执行：

```text
Downloader Agent -> Paper Reader Agent -> Idea Improver Agent
```

---

## 9. Output Check / 输出检查

After the run is complete, check / 运行结束后检查：

```bash
ls ideas/idea_001_world_model_vla/reports
```

It should contain / 应该包含：

```text
download_report.md
paper_summaries/
literature_review.md
papers.json
idea_improvement.md
idea_evaluation.md
run_summary.md
```

View each paper summary / 查看每篇论文总结：

```bash
ls ideas/idea_001_world_model_vla/reports/paper_summaries
```

View the final summary / 查看最终摘要：

```bash
cat ideas/idea_001_world_model_vla/reports/run_summary.md
```

View idea improvement / 查看 idea 改进：

```bash
less ideas/idea_001_world_model_vla/reports/idea_improvement.md
```

View idea evaluation / 查看 idea 评估：

```bash
less ideas/idea_001_world_model_vla/reports/idea_evaluation.md
```

View literature review / 查看文献综述：

```bash
less ideas/idea_001_world_model_vla/reports/literature_review.md
```

Pretty-print JSON / 格式化查看 JSON：

```bash
python -m json.tool ideas/idea_001_world_model_vla/reports/papers.json | less
```

---

## 10. Multi-Idea Management / 多 idea 管理

Create multiple ideas / 创建多个 idea：

```bash
bash shared/scripts/create_idea.sh idea_001_world_model_vla
bash shared/scripts/create_idea.sh idea_002_semantic_slam_nav
bash shared/scripts/create_idea.sh idea_003_memory_agent
```

Run only one each time / 每次只跑一个：

```text
IDEA_DIR = ideas/idea_001_world_model_vla
```

Do not let Codex process multiple ideas at once / 不要一次让 Codex 处理多个 idea。

---

## 11. What to Do When Codex Gets Stuck / Codex 卡住时的处理

### Downloader Agent keeps searching / Downloader Agent 一直搜索

```text
Stop searching. Please immediately generate download_report.md based on the current results.
停止继续搜索。请立即基于目前已有结果生成 download_report.md。
```

### Downloader Agent keeps downloading PDFs / Downloader Agent 一直下载 PDF

```text
Do not continue downloading PDFs. Record the failed papers in errors.log, then generate download_report.md.
不要继续下载 PDF。把下载失败的论文记录到 errors.log，然后生成 download_report.md。
```

### Paper Reader Agent keeps reading papers / Paper Reader Agent 一直读论文

```text
Read at most 15 papers in depth. Please immediately generate the existing paper_summaries, literature_review.md, and papers.json.
最多深度阅读 15 篇。请立即生成已有论文的 paper_summaries、literature_review.md 和 papers.json。
```

### Idea Improver Agent wants to search for more papers / Idea Improver Agent 想搜索更多论文

```text
Do not do another large-scale literature search. Please complete idea_improvement.md and idea_evaluation.md based on paper_summaries, literature_review.md, and papers.json.
不要重新做大规模文献搜索。请基于 paper_summaries、literature_review.md 和 papers.json 完成 idea_improvement.md 和 idea_evaluation.md。
```

### Want to enter the reproduction stage / 想进入复现阶段

```text
Reproduction is forbidden at the current stage. Do not write code or run experiments. Please only generate run_summary.md and then stop.
当前阶段禁止复现。不要写代码，不要跑实验。请只生成 run_summary.md，然后停止。
```

---

## 12. Stop Condition / 停止条件

The whole task is considered complete when the following files all exist / 整个任务完成标准：

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

After all these files exist, Codex should stop / 这些文件都存在后，Codex 应该停止。

---

## 13. Suggestions for the Next Stage / 后续阶段建议

After the current stage ends, read / 当前阶段结束后，阅读：

```text
reports/run_summary.md
reports/idea_improvement.md
reports/idea_evaluation.md
```

If the verdict is / 如果 verdict 是：

- Strong idea
- Promising but needs narrowing

you can consider entering the reproduction stage / 可以考虑进入复现阶段。

If the verdict is / 如果 verdict 是：

- Incremental
- Weak / already solved
- Not enough evidence

it is recommended to revise the idea first or redo the literature review / 建议先修改 idea 或重新做 literature review。
