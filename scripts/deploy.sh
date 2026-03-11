#!/bin/bash
################################################################################
# Deploy core agent files to Cursor IDE configuration directories.
#
# Source:  general-coding-agent/core/
# Target:  ~/.cursor/commands/agent.md    (orchestrator)
#          ~/.cursor/agents/*.md          (subagents)
#
# Usage:   ./scripts/deploy.sh
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
echo "Done. Deployed 1 command + $COUNT subagents."
