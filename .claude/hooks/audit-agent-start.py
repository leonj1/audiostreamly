#!/usr/bin/env python3
"""
Hook: Audit agent start events.
Triggered by SubagentStart event.

Input format (JSON from stdin):
{
    "session_id": "...",
    "cwd": "...",
    "subagent_name": "..."
}

This hook logs the agent start event to the audit trail.
"""

import json
import os
import sys

# Add scripts directory to path for audit_logger import
scripts_dir = os.path.join(os.path.dirname(__file__), "..", "scripts")
sys.path.insert(0, scripts_dir)

try:
    from audit_logger import log_agent_start
except ImportError:
    # Fallback if import fails - do nothing but don't block
    def log_agent_start(*args, **kwargs):
        pass


def main():
    try:
        input_data = sys.stdin.read()
        if not input_data.strip():
            sys.exit(0)

        data = json.loads(input_data)
        session_id = data.get("session_id")
        cwd = data.get("cwd")
        agent_name = data.get("subagent_name", data.get("agent_name", ""))

        if not all([session_id, cwd, agent_name]):
            sys.exit(0)

        # Validate session_id (alphanumeric, hyphen, underscore only)
        if not all(c.isalnum() or c in '-_' for c in session_id):
            sys.exit(0)

        log_agent_start(cwd, session_id, agent_name)

    except json.JSONDecodeError:
        pass
    except Exception as e:
        sys.stderr.write(f"audit-agent-start error: {e}\n")

    sys.exit(0)


if __name__ == "__main__":
    main()
