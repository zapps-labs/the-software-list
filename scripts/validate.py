#!/usr/bin/env python3
"""Validates software.json against the-software-list protocol v1."""

import json
import re
import sys
from pathlib import Path

VALID_OS = {"linux", "macos", "windows", "any"}
VALID_DETECT = {"binary", "path", "flatpak", "snap", "macos_app", "command"}
VALID_METHODS = {
    "pacman", "aur", "apt", "dnf", "zypper", "apk",
    "flatpak", "snap", "nix", "appimage",
    "brew", "brew_cask",
    "winget", "scoop", "choco",
    "vman_global", "cargo", "npm", "pipx",
    "script", "download", "github_release",
}
ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")


def main() -> int:
    path = Path(__file__).resolve().parent.parent / "software.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    errors = []

    if data.get("schema_version") != 1:
        errors.append("schema_version must be 1")

    items = data.get("software")
    if not isinstance(items, list) or not items:
        errors.append("software must be a non-empty array")
        items = []

    seen_ids = set()
    for idx, entry in enumerate(items):
        eid = entry.get("id", "")
        ctx = f"software[{idx}] ({eid or 'unnamed'})"
        if not isinstance(eid, str) or not ID_RE.match(eid):
            errors.append(f"{ctx}: invalid id")
        elif eid in seen_ids:
            errors.append(f"{ctx}: duplicate id '{eid}'")
        seen_ids.add(eid)

        for req in ("name", "summary", "category"):
            if not isinstance(entry.get(req), str) or not entry[req].strip():
                errors.append(f"{ctx}: missing or empty '{req}'")

        for di, det in enumerate(entry.get("detect", [])):
            if det.get("os") not in VALID_OS:
                errors.append(f"{ctx}.detect[{di}]: invalid os '{det.get('os')}'")
            if det.get("kind") not in VALID_DETECT:
                errors.append(f"{ctx}.detect[{di}]: invalid kind '{det.get('kind')}'")
            if not isinstance(det.get("value"), str) or not det["value"].strip():
                errors.append(f"{ctx}.detect[{di}]: missing value")

        for mi, method in enumerate(entry.get("methods", [])):
            if method.get("os") not in VALID_OS:
                errors.append(f"{ctx}.methods[{mi}]: invalid os '{method.get('os')}'")
            kind = method.get("kind")
            if kind not in VALID_METHODS:
                errors.append(f"{ctx}.methods[{mi}]: invalid kind '{kind}'")
            if kind == "script":
                if not method.get("install_cmd"):
                    errors.append(f"{ctx}.methods[{mi}]: script method needs install_cmd")
            elif kind in ("download", "appimage"):
                if not method.get("url"):
                    errors.append(f"{ctx}.methods[{mi}]: {kind} method needs url")
            else:
                if not method.get("package"):
                    errors.append(f"{ctx}.methods[{mi}]: {kind} method needs package")

        seen_cfgs = set()
        for ci, cfg in enumerate(entry.get("configs", [])):
            cid = cfg.get("id", "")
            if not cid or cid in seen_cfgs:
                errors.append(f"{ctx}.configs[{ci}]: missing or duplicate config id")
            seen_cfgs.add(cid)

    if errors:
        for e in errors:
            print(f"ERROR: {e}", file=sys.stderr)
        return 1

    print(f"OK: validated {len(items)} software entries in {path.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
