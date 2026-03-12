#!/bin/bash
################################################################################
# Deploy core agent files to Cursor IDE configuration directories,
# and optionally archive core/ into the current iteration.
#
# Source:  general-coding-agent/core/
# Target:  ~/.cursor/commands/agent.md    (orchestrator)
#          ~/.cursor/agents/*.md          (subagents)
#
# Usage:
#   ./scripts/deploy.sh              # deploy to Cursor only
#   ./scripts/deploy.sh --archive    # deploy + save core/ to current iteration
################################################################################

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
CORE_DIR="$PROJECT_ROOT/core"

CURSOR_COMMANDS="$HOME/.cursor/commands"
CURSOR_AGENTS="$HOME/.cursor/agents"

if [ ! -d "$CORE_DIR" ]; then
    echo "ERROR: core/ directory not found at $CORE_DIR"
    exit 1
fi

mkdir -p "$CURSOR_COMMANDS" "$CURSOR_AGENTS"

echo "Deploying agent files to Cursor..."
echo ""

# Deploy orchestrator
if [ -f "$CORE_DIR/agent.md" ]; then
    cp "$CORE_DIR/agent.md" "$CURSOR_COMMANDS/agent.md"
    echo "  agent.md -> $CURSOR_COMMANDS/agent.md"
else
    echo "  SKIP: agent.md not found in core/"
fi

# Deploy subagents
COUNT=0
for f in "$CORE_DIR/subagents/"*.md; do
    [ -f "$f" ] || continue
    NAME=$(basename "$f")
    cp "$f" "$CURSOR_AGENTS/$NAME"
    echo "  subagents/$NAME -> $CURSOR_AGENTS/$NAME"
    COUNT=$((COUNT + 1))
done

echo ""
echo "Deployed 1 command + $COUNT subagents."

# Archive core/ to current iteration if --archive flag is set
if [ "$1" = "--archive" ]; then
    CURRENT_LINK="$PROJECT_ROOT/current"
    if [ ! -L "$CURRENT_LINK" ]; then
        echo ""
        echo "ERROR: 'current' symlink not found. Cannot archive."
        exit 1
    fi

    ITER_DIR="$(readlink "$CURRENT_LINK")"
    ARCHIVE_DIR="$PROJECT_ROOT/$ITER_DIR/files/core"

    mkdir -p "$ARCHIVE_DIR/subagents"
    cp "$CORE_DIR/agent.md" "$ARCHIVE_DIR/agent.md"
    for f in "$CORE_DIR/subagents/"*.md; do
        [ -f "$f" ] || continue
        cp "$f" "$ARCHIVE_DIR/subagents/$(basename "$f")"
    done

    echo ""
    echo "Archived core/ -> $ITER_DIR/files/core/"
fi
