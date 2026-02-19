#!/usr/bin/env python3
"""
Quick validation script for skills - minimal version

Derived from: anthropics/skills/skill-creator (Apache License 2.0)
Original: https://github.com/anthropics/skills
Modifications:
  - Added SKILL.md body line count check (warn if > 500 lines)
  - Added description quality heuristics (TODO detection, length warning)
"""

import sys
import os
import re
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None


def parse_frontmatter_manual(content: str) -> tuple[dict | None, str]:
    """Parse YAML frontmatter without PyYAML dependency."""
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return None, "Invalid frontmatter format"

    frontmatter_text = match.group(1)
    result: dict[str, str] = {}
    for line in frontmatter_text.strip().split('\n'):
        if ':' in line:
            key, _, value = line.partition(':')
            result[key.strip()] = value.strip()
    return result, ""


def validate_skill(skill_path: str) -> tuple[bool, str]:
    """Basic validation of a skill. Returns (is_valid, message)."""
    skill_path_obj = Path(skill_path)
    messages: list[str] = []
    has_error = False

    # Check SKILL.md exists
    skill_md = skill_path_obj / 'SKILL.md'
    if not skill_md.exists():
        return False, "❌ SKILL.md not found"

    # Read content
    content = skill_md.read_text()
    if not content.startswith('---'):
        return False, "❌ No YAML frontmatter found"

    # Extract frontmatter
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return False, "❌ Invalid frontmatter format"

    frontmatter_text = match.group(1)

    # Parse YAML frontmatter
    if yaml:
        try:
            frontmatter = yaml.safe_load(frontmatter_text)
            if not isinstance(frontmatter, dict):
                return False, "❌ Frontmatter must be a YAML dictionary"
        except yaml.YAMLError as e:
            return False, f"❌ Invalid YAML in frontmatter: {e}"
    else:
        frontmatter, err = parse_frontmatter_manual(content)
        if frontmatter is None:
            return False, f"❌ {err}"
        messages.append("⚠️  PyYAML not installed, using basic parser")

    # Define allowed properties
    ALLOWED_PROPERTIES = {
        'name', 'description', 'license',
        'allowed-tools', 'metadata', 'compatibility',
    }

    # Check for unexpected properties
    unexpected_keys = set(frontmatter.keys()) - ALLOWED_PROPERTIES
    if unexpected_keys:
        has_error = True
        messages.append(
            f"❌ Unexpected key(s) in frontmatter: {', '.join(sorted(unexpected_keys))}. "
            f"Allowed: {', '.join(sorted(ALLOWED_PROPERTIES))}"
        )

    # Check required fields
    if 'name' not in frontmatter:
        has_error = True
        messages.append("❌ Missing 'name' in frontmatter")
    if 'description' not in frontmatter:
        has_error = True
        messages.append("❌ Missing 'description' in frontmatter")

    # Validate name
    name = frontmatter.get('name', '')
    if not isinstance(name, str):
        has_error = True
        messages.append(f"❌ Name must be a string, got {type(name).__name__}")
    else:
        name = name.strip()
        if name:
            if not re.match(r'^[a-z0-9-]+$', name):
                has_error = True
                messages.append(f"❌ Name '{name}' should be kebab-case (lowercase letters, digits, hyphens only)")
            if name.startswith('-') or name.endswith('-') or '--' in name:
                has_error = True
                messages.append(f"❌ Name '{name}' cannot start/end with hyphen or contain consecutive hyphens")
            if len(name) > 64:
                has_error = True
                messages.append(f"❌ Name is too long ({len(name)} chars). Maximum: 64")
            # Check name matches directory name
            dir_name = skill_path_obj.name
            if name != dir_name:
                messages.append(f"⚠️  Name '{name}' does not match directory name '{dir_name}'")

    # Validate description
    description = frontmatter.get('description', '')
    if not isinstance(description, str):
        has_error = True
        messages.append(f"❌ Description must be a string, got {type(description).__name__}")
    else:
        description = description.strip()
        if description:
            if '<' in description or '>' in description:
                has_error = True
                messages.append("❌ Description cannot contain angle brackets (< or >)")
            if len(description) > 1024:
                has_error = True
                messages.append(f"❌ Description is too long ({len(description)} chars). Maximum: 1024")
            if 'TODO' in description or '[TODO' in description:
                messages.append("⚠️  Description contains TODO placeholder — update before use")
            if len(description) < 50:
                messages.append("⚠️  Description is very short — consider adding trigger keywords")

    # Validate compatibility field if present
    compatibility = frontmatter.get('compatibility', '')
    if compatibility:
        if not isinstance(compatibility, str):
            has_error = True
            messages.append(f"❌ Compatibility must be a string, got {type(compatibility).__name__}")
        elif len(compatibility) > 500:
            has_error = True
            messages.append(f"❌ Compatibility is too long ({len(compatibility)} chars). Maximum: 500")

    # Check SKILL.md body line count
    body_start = content.find('---', 3)
    if body_start != -1:
        body = content[body_start + 3:]
        body_lines = body.strip().split('\n')
        line_count = len(body_lines)
        if line_count > 500:
            messages.append(f"⚠️  SKILL.md body is {line_count} lines (recommended max: 500)")
        else:
            messages.append(f"✅ SKILL.md body: {line_count} lines (within 500-line limit)")

    if has_error:
        return False, "\n".join(messages)
    else:
        messages.insert(0, "✅ Skill is valid!")
        return True, "\n".join(messages)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python quick_validate.py <skill_directory>")
        sys.exit(1)

    valid, message = validate_skill(sys.argv[1])
    print(message)
    sys.exit(0 if valid else 1)
