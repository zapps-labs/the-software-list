<p align="center">
  <img src="assets/logo.svg" alt="the-software-list logo" width="128" height="128" />
</p>

# The Software List

An open software list that is free to be used by any app, installer or operating system. The goal is to make software more widely available, easier to find and installed.

You can add your software by modifying `software.json` and opening a pull request. Then we will validate your entry and merge it so it becomes available to the world.

The software list is for both open & closed software. We dont refuse any additions other than clearly malicious software. Although the ultimate responsibility of security stays with the user.

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
