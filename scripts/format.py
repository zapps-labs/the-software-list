#!/usr/bin/env python3
"""Formats software.json in a compact, human-readable layout (inline small arrays/objects)."""

import json
from pathlib import Path


def compact(val) -> str:
    return json.dumps(val, ensure_ascii=False, separators=(", ", ": "))


def format_entry(entry: dict) -> str:
    lines = ["    {"]
    items = list(entry.items())
    for idx, (key, val) in enumerate(items):
        comma = "," if idx < len(items) - 1 else ""
        if key in ("detect", "methods", "configs") and isinstance(val, list) and val:
            lines.append(f'      "{key}": [')
            for sub_i, sub in enumerate(val):
                sub_comma = "," if sub_i < len(val) - 1 else ""
                lines.append(f"        {compact(sub)}{sub_comma}")
            lines.append(f"      ]{comma}")
        else:
            lines.append(f'      "{key}": {compact(val)}{comma}')
    lines.append("    }")
    return "\n".join(lines)


def format_catalog(data: dict) -> str:
    lines = [
        "{",
        f'  "schema_version": {compact(data["schema_version"])},',
        f'  "name": {compact(data.get("name", "the-software-list"))},',
    ]
    categories = data.get("categories")
    if isinstance(categories, dict):
        lines.append('  "categories": {')
        cat_items = sorted(categories.items(), key=lambda kv: kv[0])
        for idx, (ckey, clabel) in enumerate(cat_items):
            comma = "," if idx < len(cat_items) - 1 else ""
            lines.append(f'    {compact(ckey)}: {compact(clabel)}{comma}')
        lines.append("  },")
    lines.append('  "software": [')
    software = sorted(data["software"], key=lambda x: x["name"].lower())
    for idx, entry in enumerate(software):
        comma = "," if idx < len(software) - 1 else ""
        block = format_entry(entry)
        lines.append(f"{block}{comma}")
    lines.append("  ]")
    lines.append("}")
    return "\n".join(lines) + "\n"


def main() -> int:
    path = Path(__file__).resolve().parent.parent / "software.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    formatted = format_catalog(data)
    path.write_text(formatted, encoding="utf-8")
    line_count = formatted.count("\n")
    print(f"Formatted {path.name}: {len(data['software'])} entries, {line_count} lines, {len(formatted)} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
