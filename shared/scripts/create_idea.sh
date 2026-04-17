#!/usr/bin/env bash
set -e

if [ -z "$1" ]; then
  echo "Usage: bash shared/scripts/create_idea.sh idea_001_short_name"
  exit 1
fi

IDEA_NAME="$1"
IDEA_DIR="ideas/$IDEA_NAME"

if [ -d "$IDEA_DIR" ]; then
  echo "Error: $IDEA_DIR already exists."
  exit 1
fi

mkdir -p "$IDEA_DIR"/{inputs,papers/pdf,papers/metadata,reports/paper_summaries,reports,logs}
cp shared/templates/idea_template.md "$IDEA_DIR/inputs/idea.md"

touch "$IDEA_DIR/logs/downloader_agent.log"
touch "$IDEA_DIR/logs/paper_reader_agent.log"
touch "$IDEA_DIR/logs/idea_improver_agent.log"
touch "$IDEA_DIR/logs/errors.log"

echo "Created: $IDEA_DIR"
echo "Edit this file: $IDEA_DIR/inputs/idea.md"
