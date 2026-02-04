#!/usr/bin/env python3
"""
Centralized audit logging utility for Claude Code hooks.

Provides functions to:
- Initialize audit log for a session
- Append events to the audit log
- Track parent-child relationships for agents

Usage from hooks:
    # Python hooks can import directly
    from audit_logger import log_agent_stop, log_hook_executed
    log_agent_stop(cwd, session_id, "coder", status="success")

    # Shell hooks can call via CLI
    python3 .claude/scripts/audit_logger.py log_agent_stop \\
        --cwd /path/to/project \\
        --session-id abc123 \\
        --agent coder \\
        --status success
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


def get_state_dir(cwd: str) -> Path:
    """Get the state directory path, creating if needed."""
    state_dir = Path(cwd) / ".claude" / ".state"
    state_dir.mkdir(parents=True, exist_ok=True)
    return state_dir


def get_reports_dir(cwd: str) -> Path:
    """Get the reports directory path, creating if needed."""
    reports_dir = Path(cwd) / ".claude" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    return reports_dir


def get_audit_log_path(cwd: str, session_id: str) -> Path:
    """Get path to the audit log file."""
    return get_state_dir(cwd) / f"audit-log-{session_id}.jsonl"


def get_agent_stack_path(cwd: str, session_id: str) -> Path:
    """Get path to the agent stack file (tracks nesting)."""
    return get_state_dir(cwd) / f"agent-stack-{session_id}.json"


def validate_session_id(session_id: str) -> bool:
    """Validate session_id format (alphanumeric, hyphen, underscore only)."""
    if not session_id:
        return False
    return all(c.isalnum() or c in '-_' for c in session_id)


def log_event(cwd: str, session_id: str, event_type: str, **data) -> None:
    """Append an event to the audit log."""
    if not validate_session_id(session_id):
        return

    log_path = get_audit_log_path(cwd, session_id)

    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event": event_type,
        "session_id": session_id,
        **data
    }

    with open(log_path, "a") as f:
        f.write(json.dumps(event) + "\n")


def push_agent(cwd: str, session_id: str, agent_name: str) -> tuple[Optional[str], int]:
    """Push agent onto stack, return (parent, depth)."""
    if not validate_session_id(session_id):
        return None, 0

    stack_path = get_agent_stack_path(cwd, session_id)

    stack = []
    if stack_path.exists():
        try:
            stack = json.loads(stack_path.read_text())
        except json.JSONDecodeError:
            stack = []

    parent = stack[-1] if stack else None
    depth = len(stack)
    stack.append(agent_name)

    stack_path.write_text(json.dumps(stack))
    return parent, depth


def pop_agent(cwd: str, session_id: str) -> Optional[str]:
    """Pop agent from stack, return the popped agent name."""
    if not validate_session_id(session_id):
        return None

    stack_path = get_agent_stack_path(cwd, session_id)

    if not stack_path.exists():
        return None

    try:
        stack = json.loads(stack_path.read_text())
    except json.JSONDecodeError:
        return None

    if not stack:
        return None

    agent = stack.pop()
    stack_path.write_text(json.dumps(stack))
    return agent


def log_command_start(cwd: str, session_id: str, command: str, arguments: str = "") -> None:
    """Log a slash command invocation."""
    log_event(cwd, session_id, "command_start", command=command, arguments=arguments)


def log_agent_start(cwd: str, session_id: str, agent_name: str) -> None:
    """Log agent start and track in stack."""
    parent, depth = push_agent(cwd, session_id, agent_name)
    log_event(cwd, session_id, "agent_start", agent=agent_name, parent=parent, depth=depth)


def log_agent_stop(cwd: str, session_id: str, agent_name: str, duration_ms: int = 0, status: str = "success") -> None:
    """Log agent stop and remove from stack."""
    pop_agent(cwd, session_id)
    log_event(cwd, session_id, "agent_stop", agent=agent_name, duration_ms=duration_ms, status=status)


def log_hook_executed(cwd: str, session_id: str, hook_name: str, trigger_agent: str, outcome: str = "continue") -> None:
    """Log hook execution."""
    log_event(cwd, session_id, "hook_executed", hook=hook_name, trigger_agent=trigger_agent, outcome=outcome)


def log_skill_discovery(cwd: str, session_id: str, query: str, matched_skills: list, route_type: str = "") -> None:
    """Log skill discovery event."""
    log_event(cwd, session_id, "skill_discovery", query=query, matched_skills=matched_skills, route_type=route_type)


def cli_main():
    """CLI interface for shell hooks to call audit functions."""
    parser = argparse.ArgumentParser(description="Audit logger for Claude Code hooks")
    parser.add_argument("action", choices=[
        "log_command_start",
        "log_agent_start",
        "log_agent_stop",
        "log_hook_executed",
        "log_skill_discovery"
    ], help="Action to perform")
    parser.add_argument("--cwd", required=True, help="Working directory")
    parser.add_argument("--session-id", required=True, help="Session ID")
    parser.add_argument("--command", help="Command name (for log_command_start)")
    parser.add_argument("--arguments", default="", help="Command arguments (for log_command_start)")
    parser.add_argument("--agent", help="Agent name")
    parser.add_argument("--status", default="success", help="Agent status (for log_agent_stop)")
    parser.add_argument("--duration-ms", type=int, default=0, help="Duration in ms (for log_agent_stop)")
    parser.add_argument("--hook", help="Hook name (for log_hook_executed)")
    parser.add_argument("--trigger-agent", help="Trigger agent (for log_hook_executed)")
    parser.add_argument("--outcome", default="continue", help="Hook outcome (for log_hook_executed)")
    parser.add_argument("--query", help="Query string (for log_skill_discovery)")
    parser.add_argument("--matched-skills", help="Comma-separated skills (for log_skill_discovery)")
    parser.add_argument("--route-type", default="", help="Route type (for log_skill_discovery)")

    args = parser.parse_args()

    if args.action == "log_command_start":
        if not args.command:
            parser.error("--command is required for log_command_start")
        log_command_start(args.cwd, args.session_id, args.command, args.arguments)

    elif args.action == "log_agent_start":
        if not args.agent:
            parser.error("--agent is required for log_agent_start")
        log_agent_start(args.cwd, args.session_id, args.agent)

    elif args.action == "log_agent_stop":
        if not args.agent:
            parser.error("--agent is required for log_agent_stop")
        log_agent_stop(args.cwd, args.session_id, args.agent, args.duration_ms, args.status)

    elif args.action == "log_hook_executed":
        if not args.hook or not args.trigger_agent:
            parser.error("--hook and --trigger-agent are required for log_hook_executed")
        log_hook_executed(args.cwd, args.session_id, args.hook, args.trigger_agent, args.outcome)

    elif args.action == "log_skill_discovery":
        if not args.query:
            parser.error("--query is required for log_skill_discovery")
        skills = args.matched_skills.split(",") if args.matched_skills else []
        log_skill_discovery(args.cwd, args.session_id, args.query, skills, args.route_type)


if __name__ == "__main__":
    cli_main()
