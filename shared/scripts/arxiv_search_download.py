#!/usr/bin/env python3
"""arXiv search and download helper / arXiv 搜索与下载辅助脚本."""

import argparse
import json
import re
from pathlib import Path

import arxiv


def safe_filename(name: str, max_len: int = 120) -> str:
    """Make a safe filename / 生成安全文件名。"""
    name = re.sub(r"[^\w\s\-\.]", "_", name)
    name = re.sub(r"\s+", "_", name.strip())
    return name[:max_len]


def read_idea_keywords(idea_path: Path) -> str:
    """Read keyword-rich text from the idea file / 从 idea 文件中读取关键词密集片段。"""
    text = idea_path.read_text(encoding="utf-8", errors="ignore")
    lower = text.lower()
    if "## keywords" in lower:
        idx = lower.find("## keywords")
        return text[idx : idx + 1000]
    return text[:3000]


def build_query(raw_text: str) -> str:
    """Build a lightweight query from idea text / 根据 idea 内容构造轻量查询。"""
    candidates = [
        "vision language action",
        "VLA",
        "embodied agent",
        "robot manipulation",
        "world model",
        "latent planning",
        "semantic map",
        "SLAM",
        "navigation",
        "reinforcement learning",
        "robot learning",
        "diffusion policy",
        "large language model",
        "vision language navigation",
        "open vocabulary",
        "semantic mapping",
        "language conditioned robot",
        "long horizon manipulation",
    ]

    raw_lower = raw_text.lower()
    keywords = [k for k in candidates if k.lower() in raw_lower]

    if not keywords:
        keywords = ["robot learning", "embodied agent", "robot manipulation"]

    return " OR ".join([f'all:"{k}"' for k in keywords[:8]])


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Search arXiv and optionally download PDFs for one idea directory. "
            "/ 为某个 idea 目录搜索 arXiv 并可选下载 PDF。"
        )
    )
    parser.add_argument(
        "--idea-dir",
        required=True,
        help="Example / 示例: ideas/idea_001_world_model_vla",
    )
    parser.add_argument("--max-results", type=int, default=25, help="Maximum papers / 最大论文数")
    parser.add_argument("--query", type=str, default=None, help="Manual arXiv query / 手动 arXiv 查询")
    parser.add_argument("--download-pdf", action="store_true", help="Download PDFs / 下载 PDF")
    parser.add_argument("--no-download-pdf", action="store_true", help="Skip PDF download / 跳过 PDF 下载")

    args = parser.parse_args()

    idea_dir = Path(args.idea_dir)
    idea_path = idea_dir / "inputs" / "idea.md"
    pdf_dir = idea_dir / "papers" / "pdf"
    meta_dir = idea_dir / "papers" / "metadata"
    log_dir = idea_dir / "logs"

    pdf_dir.mkdir(parents=True, exist_ok=True)
    meta_dir.mkdir(parents=True, exist_ok=True)
    log_dir.mkdir(parents=True, exist_ok=True)

    errors_log = log_dir / "errors.log"

    if not idea_path.exists():
        raise FileNotFoundError(f"Missing idea file / 缺少 idea 文件: {idea_path}")

    if args.query:
        query = args.query
    else:
        idea_keywords = read_idea_keywords(idea_path)
        query = build_query(idea_keywords)

    should_download_pdf = args.download_pdf and not args.no_download_pdf

    print(f"[INFO] IDEA_DIR / idea 目录: {idea_dir}")
    print(f"[INFO] arXiv query / arXiv 查询: {query}")
    print(f"[INFO] download_pdf / 是否下载 PDF: {should_download_pdf}")

    client = arxiv.Client()
    search = arxiv.Search(
        query=query,
        max_results=args.max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate,
    )

    papers = []

    for idx, result in enumerate(client.results(search), start=1):
        item = {
            "index": idx,
            "title": result.title,
            "authors": [str(a) for a in result.authors],
            "published": result.published.isoformat() if result.published else None,
            "updated": result.updated.isoformat() if result.updated else None,
            "summary": result.summary,
            "entry_id": result.entry_id,
            "pdf_url": result.pdf_url,
            "primary_category": result.primary_category,
            "categories": result.categories,
            "downloaded_pdf": None,
            "download_error": None,
            "source": "arxiv",
        }

        print(f"
[{idx}] {result.title}")
        print(f"    arXiv: {result.entry_id}")
        print(f"    PDF:   {result.pdf_url}")

        if should_download_pdf:
            filename = safe_filename(f"{idx:02d}_{result.title}") + ".pdf"
            pdf_path = pdf_dir / filename

            try:
                result.download_pdf(filename=str(pdf_path))
                item["downloaded_pdf"] = str(pdf_path)
                print(f"    Downloaded / 已下载: {pdf_path}")
            except Exception as e:
                item["download_error"] = str(e)
                with errors_log.open("a", encoding="utf-8") as f:
                    f.write(f"[PDF_DOWNLOAD_FAILED] {result.title}
")
                    f.write(f"URL: {result.pdf_url}
")
                    f.write(f"ERROR: {e}

")
                print(f"    Download failed / 下载失败: {e}")

        papers.append(item)

    output_path = meta_dir / "arxiv_results.json"
    output_path.write_text(
        json.dumps(
            {
                "idea_dir": str(idea_dir),
                "query": query,
                "max_results": args.max_results,
                "num_results": len(papers),
                "papers": papers,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(f"
[DONE] Saved metadata / 元数据已保存到: {output_path}")
    print(f"[DONE] Papers found / 找到论文数: {len(papers)}")


if __name__ == "__main__":
    main()
