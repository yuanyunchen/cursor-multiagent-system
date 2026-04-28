#!/bin/bash
################################################################################
# Deploy agent definitions and skills to Cursor IDE directories.
#
# Source -> Target mapping:
#   core/agent.md            -> ~/.cursor/commands/agent.md
#   core/subagents/*.md      -> ~/.cursor/agents/*.md
#   skills/*                 -> ~/.cursor/skills/*
#
# Usage:   ./scripts/deploy.sh [--archive [<version>]]
#   --archive            snapshot core/, skills/, scripts/ into
#                        iterations/current/files/{core,skills,scripts}/
#   --archive <version>  same snapshot, written to
#                        iterations/<version>/files/{core,skills,scripts}/
#                        (use on every commit so the version is reconstructible)
################################################################################

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
CORE_DIR="$PROJECT_ROOT/core"
SKILLS_DIR="$PROJECT_ROOT/skills"

CURSOR_COMMANDS="$HOME/.cursor/commands"
CURSOR_AGENTS="$HOME/.cursor/agents"
CURSOR_SKILLS="$HOME/.cursor/skills"
LEGACY_SKILLS=("report-builder")
if [ ! -d "$CORE_DIR" ]; then
    echo "ERROR: core/ directory not found at $CORE_DIR"
    exit 1
fi

mkdir -p "$CURSOR_COMMANDS" "$CURSOR_AGENTS"

echo "Deploying agent system to Cursor..."
echo ""

# --- Core: orchestrator + subagents ---
echo "[core]"
if [ -f "$CORE_DIR/agent.md" ]; then
    cp "$CORE_DIR/agent.md" "$CURSOR_COMMANDS/agent.md"
    echo "  agent.md -> $CURSOR_COMMANDS/agent.md"
else
    echo "  SKIP: agent.md not found in core/"
fi

AGENT_COUNT=0
for f in "$CORE_DIR/subagents/"*.md; do
    [ -f "$f" ] || continue
    NAME=$(basename "$f")
    cp "$f" "$CURSOR_AGENTS/$NAME"
    echo "  subagents/$NAME -> $CURSOR_AGENTS/$NAME"
    AGENT_COUNT=$((AGENT_COUNT + 1))
done

# --- Skills ---
SKILL_COUNT=0
if [ -d "$SKILLS_DIR" ]; then
    echo ""
    echo "[skills]"
    for legacy in "${LEGACY_SKILLS[@]}"; do
        if [ ! -d "$SKILLS_DIR/$legacy" ] && [ -d "$CURSOR_SKILLS/$legacy" ]; then
            rm -rf "$CURSOR_SKILLS/$legacy"
            echo "  removed legacy skill $CURSOR_SKILLS/$legacy"
        fi
    done
    for skill_dir in "$SKILLS_DIR"/*/; do
        [ -d "$skill_dir" ] || continue
        SKILL_NAME=$(basename "$skill_dir")
        mkdir -p "$CURSOR_SKILLS/$SKILL_NAME"
        rsync -a --delete "$skill_dir" "$CURSOR_SKILLS/$SKILL_NAME/"
        echo "  skills/$SKILL_NAME/ -> $CURSOR_SKILLS/$SKILL_NAME/"
        SKILL_COUNT=$((SKILL_COUNT + 1))
    done
fi

# --- Archive (optional) ---
if [ "$1" = "--archive" ]; then
    ARCHIVE_VERSION="${2:-current}"
    ARCHIVE_ROOT="$PROJECT_ROOT/iterations/$ARCHIVE_VERSION/files"
    mkdir -p "$ARCHIVE_ROOT"
    echo ""
    echo "[archive] target: iterations/$ARCHIVE_VERSION/files/"
    for src in "core" "skills" "scripts"; do
        SRC_PATH="$PROJECT_ROOT/$src"
        [ -d "$SRC_PATH" ] || continue
        DST_PATH="$ARCHIVE_ROOT/$src"
        mkdir -p "$DST_PATH"
        rsync -a --delete \
            --exclude='__pycache__' --exclude='*.pyc' --exclude='.DS_Store' \
            "$SRC_PATH/" "$DST_PATH/"
        echo "  $src/ -> iterations/$ARCHIVE_VERSION/files/$src/"
    done
fi

echo ""
echo "Done. Deployed 1 command + $AGENT_COUNT subagents + $SKILL_COUNT skills."
