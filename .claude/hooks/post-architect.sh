#!/bin/bash
# Post-architect hook
# This hook runs after the architect agent completes
# It signals to the orchestrator that the DRAFT spec is ready for alternative solutions

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
    --agent "architect" \
    --status success 2>/dev/null || true

  python3 "$CWD/.claude/scripts/audit_logger.py" log_hook_executed \
    --cwd "$CWD" \
    --session-id "$SESSION_ID" \
    --hook "post-architect.sh" \
    --trigger-agent "architect" \
    --outcome continue 2>/dev/null || true
fi

cat <<EOF
{
  "continue": true,
  "systemMessage": "Architect agent completed. DRAFT spec created. Invoke alternate-solutions agent to generate 3 alternative architectural approaches."
}
EOF
