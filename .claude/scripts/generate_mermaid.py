#!/usr/bin/env python3
"""
Generate Mermaid sequence diagram from audit log.

Reads: .claude/.state/audit-log-{session_id}.jsonl
Writes: .claude/reports/flow-{session_id}.md
        .claude/reports/flow-{session_id}.mermaid

Usage:
    # With session_id from stdin (hook mode)
    echo '{"session_id":"abc123","cwd":"/path"}' | python3 generate_mermaid.py

    # With session_id as argument
    python3 generate_mermaid.py --session-id abc123 --cwd /path

    # Auto-detect most recent log
    python3 generate_mermaid.py --cwd /path
"""

import argparse
import json
import os
import sys
from collections import OrderedDict
from datetime import datetime
from pathlib import Path


def parse_audit_log(log_path: Path) -> list[dict]:
    """Parse JSONL audit log into list of events."""
    events = []
    with open(log_path) as f:
        for line in f:
            if line.strip():
                try:
                    events.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return events


def generate_agent_abbreviation(agent_name: str, existing: set) -> str:
    """Generate a unique abbreviation for an agent name."""
    # Try first letters of each word
    words = agent_name.replace("-", " ").replace("_", " ").split()
    abbrev = "".join(word[0].upper() for word in words if word)

    # If abbreviation exists, add numbers
    if abbrev in existing:
        i = 2
        while f"{abbrev}{i}" in existing:
            i += 1
        abbrev = f"{abbrev}{i}"

    return abbrev


def escape_mermaid_text(text: str) -> str:
    """Escape special characters for Mermaid diagram text."""
    # Mermaid has issues with certain characters in labels
    text = text.replace('"', "'")
    text = text.replace("\n", " ")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    # Truncate long text
    if len(text) > 50:
        text = text[:47] + "..."
    return text


def generate_mermaid(events: list[dict]) -> str:
    """Generate Mermaid sequence diagram from events."""
    # Collect unique agents in order of appearance
    agents = OrderedDict()
    agents["Orchestrator"] = "O"
    existing_abbrevs = {"O"}

    for event in events:
        if event.get("event") == "agent_start":
            agent = event.get("agent", "")
            if agent and agent not in agents:
                abbrev = generate_agent_abbreviation(agent, existing_abbrevs)
                agents[agent] = abbrev
                existing_abbrevs.add(abbrev)

    # Build diagram
    lines = ["sequenceDiagram"]

    # Add participants
    for agent, abbrev in agents.items():
        display_name = agent.replace("-", " ").replace("_", " ").title()
        lines.append(f"    participant {abbrev} as {display_name}")

    lines.append("")

    # Track active agents for activate/deactivate
    active_agents = set()

    # Process events
    for event in events:
        event_type = event.get("event")

        if event_type == "command_start":
            cmd = event.get("command", "")
            args = escape_mermaid_text(event.get("arguments", "")[:40])
            lines.append(f"    Note over O: /{cmd} {args}")

        elif event_type == "agent_start":
            agent = event.get("agent", "")
            parent = event.get("parent")
            abbrev = agents.get(agent, "X")

            from_actor = agents.get(parent, "O") if parent else "O"
            lines.append(f"    {from_actor}->>{abbrev}: invoke")
            lines.append(f"    activate {abbrev}")
            active_agents.add(agent)

        elif event_type == "agent_stop":
            agent = event.get("agent", "")
            abbrev = agents.get(agent, "X")
            status = event.get("status", "success")

            if agent in active_agents:
                lines.append(f"    {abbrev}-->>O: {status}")
                lines.append(f"    deactivate {abbrev}")
                active_agents.discard(agent)

        elif event_type == "hook_executed":
            hook = event.get("hook", "")
            # Clean up hook name for display
            hook_display = hook.replace(".sh", "").replace(".py", "").replace("post-", "")
            trigger = event.get("trigger_agent", "")
            abbrev = agents.get(trigger, "O")
            lines.append(f"    Note right of {abbrev}: hook: {hook_display}")

        elif event_type == "skill_discovery":
            skills = event.get("matched_skills", [])
            if skills:
                skills_str = ", ".join(skills[:3])
                if len(skills) > 3:
                    skills_str += "..."
                lines.append(f"    Note over O: skills: {skills_str}")

    return "\n".join(lines)


def generate_audit_summary(events: list[dict]) -> str:
    """Generate a human-readable audit summary."""
    lines = ["## Chronological Audit Log", ""]

    for i, event in enumerate(events, 1):
        timestamp = event.get("timestamp", "")
        event_type = event.get("event", "")

        # Format timestamp for display
        try:
            dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
            time_str = dt.strftime("%H:%M:%S.%f")[:-3]
        except (ValueError, AttributeError):
            time_str = timestamp

        if event_type == "command_start":
            cmd = event.get("command", "")
            args = event.get("arguments", "")
            lines.append(f"| {i} | {time_str} | **COMMAND** | `/{cmd}` | {args[:60]} |")

        elif event_type == "agent_start":
            agent = event.get("agent", "")
            parent = event.get("parent", "orchestrator")
            depth = event.get("depth", 0)
            indent = "→ " * depth
            lines.append(f"| {i} | {time_str} | **AGENT START** | {indent}`{agent}` | parent: {parent or 'orchestrator'} |")

        elif event_type == "agent_stop":
            agent = event.get("agent", "")
            status = event.get("status", "")
            duration = event.get("duration_ms", 0)
            lines.append(f"| {i} | {time_str} | **AGENT STOP** | `{agent}` | status: {status}, duration: {duration}ms |")

        elif event_type == "hook_executed":
            hook = event.get("hook", "")
            trigger = event.get("trigger_agent", "")
            outcome = event.get("outcome", "")
            lines.append(f"| {i} | {time_str} | **HOOK** | `{hook}` | trigger: {trigger}, outcome: {outcome} |")

        elif event_type == "skill_discovery":
            skills = event.get("matched_skills", [])
            route_type = event.get("route_type", "")
            lines.append(f"| {i} | {time_str} | **SKILL** | {', '.join(skills)} | route: {route_type} |")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate Mermaid diagram from audit log")
    parser.add_argument("--session-id", help="Session ID")
    parser.add_argument("--cwd", help="Working directory")

    args = parser.parse_args()

    # Try to get input from stdin first (hook mode)
    session_id = args.session_id
    cwd = args.cwd

    try:
        # Check if stdin has data (non-blocking)
        import select
        if select.select([sys.stdin], [], [], 0.0)[0]:
            input_data = sys.stdin.read()
            if input_data.strip():
                try:
                    data = json.loads(input_data)
                    session_id = session_id or data.get("session_id")
                    cwd = cwd or data.get("cwd")
                except json.JSONDecodeError:
                    pass
    except Exception:
        pass

    # Default cwd to current directory
    cwd = cwd or os.getcwd()

    # Find the audit log
    state_dir = Path(cwd) / ".claude" / ".state"

    if session_id:
        log_path = state_dir / f"audit-log-{session_id}.jsonl"
        if not log_path.exists():
            print(f"Audit log not found: {log_path}", file=sys.stderr)
            sys.exit(0)
    else:
        # Find most recent audit log
        logs = list(state_dir.glob("audit-log-*.jsonl")) if state_dir.exists() else []
        if not logs:
            print("No audit logs found", file=sys.stderr)
            sys.exit(0)
        log_path = max(logs, key=lambda p: p.stat().st_mtime)
        session_id = log_path.stem.replace("audit-log-", "")

    # Parse events
    events = parse_audit_log(log_path)
    if not events:
        print(f"No events in audit log: {log_path}", file=sys.stderr)
        sys.exit(0)

    # Generate diagram
    mermaid = generate_mermaid(events)

    # Generate audit summary
    audit_summary = generate_audit_summary(events)

    # Create reports directory
    reports_dir = Path(cwd) / ".claude" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    # Calculate summary stats
    start_time = events[0].get("timestamp", "") if events else ""
    end_time = events[-1].get("timestamp", "") if events else ""
    agent_count = len([e for e in events if e.get("event") == "agent_start"])
    hook_count = len([e for e in events if e.get("event") == "hook_executed"])
    command = next((e.get("command", "") for e in events if e.get("event") == "command_start"), "")

    # Write markdown file with embedded Mermaid
    output_path = reports_dir / f"flow-{session_id}.md"

    content = f"""# Pipeline Flow Report

**Session ID**: `{session_id}`
**Command**: `/{command}`
**Started**: {start_time}
**Ended**: {end_time}
**Agents Invoked**: {agent_count}
**Hooks Executed**: {hook_count}

---

## Sequence Diagram

```mermaid
{mermaid}
```

---

{audit_summary}

---

## Raw Audit Log

See: `.claude/.state/audit-log-{session_id}.jsonl`
"""

    output_path.write_text(content)
    print(f"Generated: {output_path}", file=sys.stderr)

    # Also write raw mermaid file
    raw_path = reports_dir / f"flow-{session_id}.mermaid"
    raw_path.write_text(mermaid)
    print(f"Generated: {raw_path}", file=sys.stderr)

    # Output success for hook
    print(json.dumps({
        "continue": True,
        "systemMessage": f"Audit report generated: .claude/reports/flow-{session_id}.md"
    }))


if __name__ == "__main__":
    main()
