#!/bin/bash
# Post-alternate-solutions hook
# This hook runs after the alternate-solutions agent completes
# It signals to the orchestrator that alternatives are ready for evaluation

set -e

# Parse the hook input from stdin
HOOK_INPUT=$(cat)

# Extract session info
SESSION_ID=$(echo "$HOOK_INPUT" | jq -r '.session_id' 2>/dev/null) || SESSION_ID=""
CWD=$(echo "$HOOK_INPUT" | jq -r '.cwd' 2>/dev/null) || CWD=""
SUBAGENT_NAME=$(echo "$HOOK_INPUT" | jq -r '.subagent_name // empty' 2>/dev/null) || SUBAGENT_NAME=""

# Log to audit trail if we have valid session info
if [[ "$SESSION_ID" =~ ^[a-zA-Z0-9_-]+$ ]] && [ -n "$CWD" ]; then
  python3 "$CWD/.claude/scripts/audit_logger.py" log_agent_stop \
    --cwd "$CWD" \
    --session-id "$SESSION_ID" \
    --agent "alternate-solutions" \
    --status success 2>/dev/null || true

  python3 "$CWD/.claude/scripts/audit_logger.py" log_hook_executed \
    --cwd "$CWD" \
    --session-id "$SESSION_ID" \
    --hook "post-alternate-solutions.sh" \
    --trigger-agent "alternate-solutions" \
    --outcome continue 2>/dev/null || true
fi

cat <<EOF
{
  "continue": true,
  "systemMessage": "Alternate-solutions agent completed. specs/ALTERNATIVE-SOLUTIONS.md created. Invoke architecture-evaluator agent to evaluate and select the optimal approach."
}
EOF
