<p align="center">
  <img src="assets/logo.svg" alt="the-software-list logo" width="128" height="128" />
</p>

# The Software List

An open, tool-agnostic JSON catalog of software describing how applications can be **installed**, **detected**, **updated**, **uninstalled**, and how their **configuration files** are located across Linux, macOS, and Windows.

`the-software-list` is not tied to any single app manager — it is designed to be consumed by GUI installers (such as `zapps`), CLI provisioners, dotfile managers, and AI agents.

## Files

- [`software.json`](software.json) — The canonical catalog of software entries.
- [`PROTOCOL.md`](PROTOCOL.md) — Specification of the protocol (`schema_version: 1`) for consumers and contributors.
- [`schema.json`](schema.json) — JSON Schema (Draft 2020-12) for automated validation.
- [`scripts/validate.py`](scripts/validate.py) — Standalone validator run in CI on every PR.

## Consuming the list

Fetch the latest catalog directly from GitHub:

```text
https://raw.githubusercontent.com/zapps-labs/the-software-list/main/software.json
```

## Contributing

1. Add or update an entry in `software.json` following [`PROTOCOL.md`](PROTOCOL.md).
2. Format and validate:
   ```sh
   python3 scripts/format.py
   python3 scripts/validate.py
   ```
3. Open a Pull Request.
