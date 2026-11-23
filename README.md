<p align="center">
  <img src="assets/logo.svg" alt="the-software-list logo" width="128" height="128" />
</p>

# The Software List

An open software list that is free to be used by any app, installer or operating system. The goal is to make software more widely available, easier to find and installed.

You can add your software by modifying `software.json` and opening a pull request. Then we will validate your entry and merge it so it becomes available to the world.

The software list is for both open & closed software. We dont refuse any additions other than clearly malicious software. Although the ultimate responsibility of security stays with the consumers of this list.

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

You don't need direct push access to this repository — contributions are submitted through a **Pull Request (PR)** from your own fork. You can do this either directly in your browser on GitHub or locally with Git.

### Option 1: Quick edit on GitHub (no Git required)

1. Open [`software.json`](software.json) on GitHub and click the **Edit (pencil)** icon in the top-right corner.
   - GitHub will automatically fork the repository to your account if you don't have one yet.
2. Add or update your software entry following [`PROTOCOL.md`](PROTOCOL.md).
3. Click **Commit changes...**, enter a short message (e.g. `Add MyApp`), and choose **Create a new branch for this commit and start a pull request**.
4. Click **Create pull request**. GitHub Actions will automatically run `scripts/validate.py` to check your entry.

### Option 2: Fork and edit locally (recommended for larger changes)

1. Click **Fork** in the top-right corner of this repository on GitHub to create your own copy.
2. Clone your fork and create a branch:
   ```sh
   git clone https://github.com/<your-username>/the-software-list.git
   cd the-software-list
   git checkout -b add-my-app
   ```
3. Add or update an entry in `software.json` following [`PROTOCOL.md`](PROTOCOL.md).
4. Format and validate your changes:
   ```sh
   python3 scripts/format.py
   python3 scripts/validate.py
   ```
5. Commit and push your branch to your fork:
   ```sh
   git add software.json
   git commit -m "Add MyApp"
   git push -u origin add-my-app
   ```
6. Open your fork on GitHub and click **Compare & pull request**, then submit the PR against `zapps-labs/the-software-list`.

### Example entry

```json
{
  "id": "my-app",
  "name": "My App",
  "summary": "Short one-line description of what the software does.",
  "category": "utilities",
  "homepage": "https://example.com",
  "license": "MIT",
  "tags": ["utility"],
  "detect": [
    {"os": "any", "kind": "binary", "value": "my-app"}
  ],
  "methods": [
    {"os": "linux", "kind": "pacman", "package": "my-app"},
    {"os": "macos", "kind": "brew", "package": "my-app"},
    {"os": "windows", "kind": "winget", "package": "Example.MyApp"}
  ]
}
```

Once your PR passes the automated validation check, a maintainer will review and merge it.
