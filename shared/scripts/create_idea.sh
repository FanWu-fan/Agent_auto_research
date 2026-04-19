#!/usr/bin/env bash
set -e

# Create a new idea workspace / 创建一个新的 idea 工作目录

if [ -z "$1" ]; then
  echo "Usage / 用法: bash shared/scripts/create_idea.sh idea_001_short_name"
  exit 1
fi

IDEA_NAME="$1"
IDEA_DIR="ideas/$IDEA_NAME"

if [ -d "$IDEA_DIR" ]; then
  echo "Error / 错误: $IDEA_DIR already exists / 已存在。"
  exit 1
fi

mkdir -p "$IDEA_DIR"/{inputs,papers/pdf,papers/metadata,reports/paper_summaries,reports,logs}
cp shared/templates/idea_template.md "$IDEA_DIR/inputs/idea.md"

touch "$IDEA_DIR/logs/downloader_agent.log"
touch "$IDEA_DIR/logs/paper_reader_agent.log"
touch "$IDEA_DIR/logs/idea_improver_agent.log"
touch "$IDEA_DIR/logs/errors.log"

echo "Created / 已创建: $IDEA_DIR"
echo "Edit this file / 请编辑该文件: $IDEA_DIR/inputs/idea.md"
