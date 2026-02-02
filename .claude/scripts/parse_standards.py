#!/usr/bin/env python3
"""
Parse coding standards files and create individual rule files in tmp/standards/.

Each rule file contains:
- Rule name
- Language(s) it applies to
- Detection patterns (grep/regex)
- Good/bad code examples
- Severity level
"""

import os
import re
import json
import hashlib
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class Rule:
    """A single coding standard rule."""
    id: str
    name: str
    language: str
    severity: str  # critical, minor
    description: str
    bad_patterns: list[str]  # grep patterns to find violations
    good_example: str
    bad_example: str
    fix_guidance: str


def generate_rule_id(name: str, language: str) -> str:
    """Generate unique rule ID from name and language."""
    content = f"{language}:{name}"
    return hashlib.md5(content.encode()).hexdigest()[:8]


def parse_python_standards(content: str) -> list[Rule]:
    """Extract rules from python.md by parsing markdown structure."""
    rules = []

    # Strategy: Find all ### subsections, look for BAD/GOOD marker pairs
    # Split by ### headers
    subsections = re.split(r'\n### ', content)

    for subsection in subsections[1:]:  # Skip first (before any ###)
        lines = subsection.strip().split('\n')
        if not lines:
            continue

        subsection_title = lines[0].strip()
        subsection_content = '\n'.join(lines[1:])

        # Check if has both BAD and GOOD markers
        if '❌ BAD' not in subsection_content or '✅ GOOD' not in subsection_content:
            continue

        # Extract all code blocks in this subsection
        code_blocks = list(re.finditer(r'```(?:python)?\n(.*?)```', subsection_content, re.DOTALL))

        if len(code_blocks) == 0:
            continue

        # Find BAD and GOOD code examples
        bad_example = None
        good_example = None

        for block in code_blocks:
            block_content = block.group(1)
            block_start = block.start()

            # Check if markers are INSIDE the code block (as comments)
            if '❌ BAD' in block_content or '✅ GOOD' in block_content:
                bad_lines = []
                good_lines = []
                in_bad = False
                in_good = False

                for line in block_content.split('\n'):
                    if '❌ BAD' in line:
                        in_bad = True
                        in_good = False
                        continue
                    elif '✅ GOOD' in line:
                        in_good = True
                        in_bad = False
                        continue

                    if in_bad:
                        # Stop if we hit another marker
                        if '❌' in line or '✅' in line:
                            break
                        bad_lines.append(line)
                    elif in_good:
                        good_lines.append(line)

                if bad_lines and not bad_example:
                    bad_example = '\n'.join(bad_lines).strip()
                if good_lines and not good_example:
                    good_example = '\n'.join(good_lines).strip()

            # Also check if markers are BEFORE the code block
            if not bad_example or not good_example:
                preceding_text = subsection_content[:block_start]
                recent_text = preceding_text[-200:] if len(preceding_text) > 200 else preceding_text

                if '❌ BAD' in recent_text and not bad_example:
                    bad_example = block_content.strip()
                elif '✅ GOOD' in recent_text and not good_example:
                    good_example = block_content.strip()

        if not bad_example or not good_example:
            continue

        # Determine severity
        severity = "critical"
        if "should" in subsection_content.lower():
            severity = "minor"

        # Generate rule slug
        rule_slug = re.sub(r'[^a-z0-9]+', '-', subsection_title.lower()).strip('-')

        # Extract description - look for first sentence or paragraph before examples
        desc_lines = []
        for line in lines[1:]:
            line = line.strip()
            if line and not line.startswith('```') and '❌' not in line and '✅' not in line:
                desc_lines.append(line)
                if '.' in line or len(desc_lines) > 2:
                    break

        description = ' '.join(desc_lines) if desc_lines else subsection_title

        # Generate patterns from bad example
        bad_patterns = generate_bad_patterns_from_examples(bad_example, subsection_title)

        # Extract fix guidance
        fix_guidance = extract_fix_guidance(subsection_content)

        rules.append(Rule(
            id=generate_rule_id(rule_slug, "python"),
            name=subsection_title,
            language="python",
            severity=severity,
            description=description if description else subsection_title,
            bad_patterns=bad_patterns,
            good_example=good_example,
            bad_example=bad_example,
            fix_guidance=fix_guidance if fix_guidance else "Follow the good example pattern"
        ))

    return rules


def extract_code_block(content: str, marker: str) -> str:
    """Extract code block following a marker like '✅ GOOD' or '❌ BAD'."""
    # Find marker position
    marker_pos = content.find(marker)
    if marker_pos == -1:
        return ""

    # Find the end of this marker's section (before next marker)
    remaining = content[marker_pos + len(marker):]

    # Look for next opposing marker or section boundary
    opposite_marker = '✅ GOOD' if marker == '❌ BAD' else '❌ BAD'
    next_marker_pos = remaining.find(opposite_marker)
    next_subsection = remaining.find('\n### ')
    next_section = remaining.find('\n## ')

    # Find the earliest boundary
    boundaries = [pos for pos in [next_marker_pos, next_subsection, next_section] if pos > 0]
    end_pos = min(boundaries) if boundaries else len(remaining)

    section_content = remaining[:end_pos]

    # Find code block after marker (```python or just ```)
    code_block_match = re.search(r'```(?:python)?\n(.*?)```', section_content, re.DOTALL)

    if code_block_match:
        return code_block_match.group(1).strip()

    # Try inline code
    inline_match = re.search(r'`([^`]+)`', section_content)
    if inline_match:
        return inline_match.group(1).strip()

    return ""


def generate_bad_patterns_from_examples(bad_example: str, section_title: str) -> list[str]:
    """Generate grep patterns from bad code examples."""
    patterns = []

    # Pattern generation based on section context
    if "log" in section_title.lower() or "logger" in bad_example.lower():
        # Logging patterns
        if "f\"" in bad_example or "f'" in bad_example:
            patterns.extend([
                r"logger\.\w+\(f['\"]",
                r"logging\.\w+\(f['\"]",
            ])
        if ".format(" in bad_example:
            patterns.extend([
                r"logger\.\w+\([^)]*\.format\(",
                r"logging\.\w+\([^)]*\.format\(",
            ])
        if "str(e)" in bad_example or "{e}" in bad_example:
            patterns.extend([
                r"logger\.error\([^)]*str\(e\)",
                r"logger\.error\([^)]*\{e\}",
            ])

    elif "default" in section_title.lower() or "=" in bad_example:
        # Default argument patterns
        if "def " in bad_example:
            patterns.append(r"def\s+\w+\([^)]*=(?!Form\(|Depends\()[^)]*\):")

    elif "environment" in section_title.lower() or "os.getenv" in bad_example:
        # Environment variable patterns
        patterns.extend([
            r"def\s+\w+\([^)]*\):[^}]*os\.getenv\(",
            r"def\s+\w+\([^)]*\):[^}]*os\.environ\[",
        ])

    elif "exception" in section_title.lower() and ("ValueError" in bad_example or "Exception" in bad_example):
        # Generic exception patterns
        patterns.extend([
            r"raise\s+ValueError\(",
            r"raise\s+Exception\(",
        ])

    elif "@router" in bad_example or "@app" in bad_example:
        # Route handler patterns
        if "try:" in bad_example or "except" in bad_example:
            patterns.extend([
                r"@(app|router)\.(get|post|put|delete|patch)\([^)]*\)[^{]*try:",
                r"@(app|router)\.(get|post|put|delete|patch)\([^)]*\)[^{]*except\s+\w+:",
            ])

    return patterns


def extract_fix_guidance(content: str) -> str:
    """Extract fix guidance from section content."""
    # Look for common guidance patterns
    guidance_patterns = [
        r"(?:should|must|need to|ensure)\s+([^\n.]+)",
        r"(?:use|add|move|create|remove)\s+([^\n.]+)",
    ]

    for pattern in guidance_patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            return match.group(0).strip()

    return "Follow the good example pattern"


def parse_general_standards(content: str) -> list[Rule]:
    """Extract rules from general.md."""
    rules = []

    # Rule: No Duplicate Files
    rules.append(Rule(
        id=generate_rule_id("no-duplicate-files", "general"),
        name="No Duplicate Files",
        language="general",
        severity="critical",
        description="Never create copies like .fixed, .new, .backup - fix original files",
        bad_patterns=[
            # File pattern matching, not content grep
        ],
        good_example='Edit Dockerfile directly',
        bad_example='Create Dockerfile.fixed alongside Dockerfile',
        fix_guidance="Delete duplicate file and fix the original"
    ))

    return rules


def parse_typescript_standards(content: str) -> list[Rule]:
    """Extract rules from typescript.md."""
    rules = []

    # Rule: No Default Arguments
    rules.append(Rule(
        id=generate_rule_id("no-default-arguments", "typescript"),
        name="No Default Arguments",
        language="typescript",
        severity="critical",
        description="Functions must not have default parameter values",
        bad_patterns=[
            r"function\s+\w+\([^)]*=[^)]*\)",
            r"const\s+\w+\s*=\s*\([^)]*=[^)]*\)\s*=>",
        ],
        good_example='function createUser(name: string, email: string, role: string): User',
        bad_example='function createUser(name: string, email: string, role = "user"): User',
        fix_guidance="Remove default values and update all call sites"
    ))

    # Rule: No Environment Variable Access
    rules.append(Rule(
        id=generate_rule_id("no-env-in-functions", "typescript"),
        name="No Environment Variable Access in Functions",
        language="typescript",
        severity="critical",
        description="Functions must not access process.env directly",
        bad_patterns=[
            r"function\s+\w+\([^)]*\)[^{]*\{[^}]*process\.env\.",
            r"const\s+\w+\s*=\s*\([^)]*\)\s*=>\s*\{[^}]*process\.env\.",
        ],
        good_example='function connectToDb(host: string, port: number): Connection',
        bad_example='function connectToDb(): Connection {\n  const host = process.env.DB_HOST;',
        fix_guidance="Pass configuration as parameters, read env at startup"
    ))

    return rules


def parse_golang_standards(content: str) -> list[Rule]:
    """Extract rules from golang.md."""
    rules = []

    # Rule: Context First Parameter
    rules.append(Rule(
        id=generate_rule_id("context-first", "golang"),
        name="Context as First Parameter",
        language="golang",
        severity="critical",
        description="Functions accepting context.Context must have it as the first parameter",
        bad_patterns=[
            r"func\s+\w+\([^c][^)]*,\s*ctx\s+context\.Context",
        ],
        good_example='func GetUser(ctx context.Context, userID string) (*User, error)',
        bad_example='func GetUser(userID string, ctx context.Context) (*User, error)',
        fix_guidance="Move ctx to be the first parameter"
    ))

    return rules


def parse_markdown_standards(content: str) -> list[Rule]:
    """Extract rules from markdown.md."""
    rules = []

    # Rule: Code Block Language
    rules.append(Rule(
        id=generate_rule_id("code-block-language", "markdown"),
        name="Code Blocks Must Have Language",
        language="markdown",
        severity="minor",
        description="All fenced code blocks must specify a language identifier",
        bad_patterns=[
            r"^```$",
        ],
        good_example='```python\nprint("hello")\n```',
        bad_example='```\nprint("hello")\n```',
        fix_guidance="Add language identifier after opening backticks"
    ))

    # Rule: No Skipped Headings
    rules.append(Rule(
        id=generate_rule_id("no-skipped-headings", "markdown"),
        name="No Skipped Heading Levels",
        language="markdown",
        severity="minor",
        description="Heading hierarchy must not skip levels (# followed by ### is invalid)",
        bad_patterns=[
            # Needs multi-line analysis
        ],
        good_example='# Title\n## Section\n### Subsection',
        bad_example='# Title\n### Skipped h2',
        fix_guidance="Add intermediate heading levels"
    ))

    return rules


def write_rule_file(rule: Rule, output_dir: Path) -> None:
    """Write a single rule to its own file."""
    filename = f"{rule.language}_{rule.id}_{rule.name.lower().replace(' ', '_').replace('-', '_')}.json"
    filepath = output_dir / filename

    with open(filepath, 'w') as f:
        json.dump(asdict(rule), f, indent=2)

    print(f"Created: {filepath}")


def main():
    """Parse all coding standards and create individual rule files."""
    # Setup paths
    script_dir = Path(__file__).parent
    standards_dir = script_dir.parent / "coding-standards"
    output_dir = Path("/vercel/sandbox/project/tmp/standards")

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # Clear existing rule files
    for f in output_dir.glob("*.json"):
        f.unlink()

    all_rules = []

    # Parse Python standards
    python_file = standards_dir / "python.md"
    if python_file.exists():
        content = python_file.read_text()
        rules = parse_python_standards(content)
        all_rules.extend(rules)
        print(f"Parsed {len(rules)} rules from python.md")

    # Parse General standards
    general_file = standards_dir / "general.md"
    if general_file.exists():
        content = general_file.read_text()
        rules = parse_general_standards(content)
        all_rules.extend(rules)
        print(f"Parsed {len(rules)} rules from general.md")

    # Parse TypeScript standards
    ts_file = standards_dir / "typescript.md"
    if ts_file.exists():
        content = ts_file.read_text()
        rules = parse_typescript_standards(content)
        all_rules.extend(rules)
        print(f"Parsed {len(rules)} rules from typescript.md")

    # Parse Golang standards
    go_file = standards_dir / "golang.md"
    if go_file.exists():
        content = go_file.read_text()
        rules = parse_golang_standards(content)
        all_rules.extend(rules)
        print(f"Parsed {len(rules)} rules from golang.md")

    # Parse Markdown standards
    md_file = standards_dir / "markdown.md"
    if md_file.exists():
        content = md_file.read_text()
        rules = parse_markdown_standards(content)
        all_rules.extend(rules)
        print(f"Parsed {len(rules)} rules from markdown.md")

    # Write individual rule files
    for rule in all_rules:
        write_rule_file(rule, output_dir)

    # Write summary
    summary = {
        "total_rules": len(all_rules),
        "critical_rules": len([r for r in all_rules if r.severity == "critical"]),
        "minor_rules": len([r for r in all_rules if r.severity == "minor"]),
        "by_language": {}
    }
    for rule in all_rules:
        lang = rule.language
        if lang not in summary["by_language"]:
            summary["by_language"][lang] = []
        summary["by_language"][lang].append(rule.id)

    summary_path = output_dir / "_summary.json"
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)

    print(f"\nTotal: {len(all_rules)} rules written to {output_dir}")
    print(f"Summary: {summary_path}")


if __name__ == "__main__":
    main()
