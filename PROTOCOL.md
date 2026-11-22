# The Software List Protocol (v1)

This document defines the open JSON protocol used by `software.json` so any software manager, provisioner, or package tool can read a shared catalog of software definitions.

## Top-Level Structure

```json
{
  "schema_version": 1,
  "name": "the-software-list",
  "software": [ ... ]
}
```

- `schema_version` (`integer`, required): Protocol version. Currently `1`. Consumers should ignore unknown fields to stay forward-compatible.
- `name` (`string`, optional): Catalog identifier.
- `software` (`array`, required): List of software entries sorted or indexed by unique `id`.

## Software Entry

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `id` | `string` | Yes | Unique lowercase slug (`^[a-z0-9][a-z0-9-]*$`), e.g. `"neovim"`. |
| `name` | `string` | Yes | Human-readable display name, e.g. `"Neovim"`. |
| `summary` | `string` | Yes | Concise one-line description. |
| `category` | `string` | Yes | Primary category (`Browsers`, `CLI Tools`, `Communication`, `Development`, `Graphics`, `Media`, `Productivity`, `System`, `Terminals`, `Utilities`). |
| `homepage` | `string` | No | Official website URL (`https://...`). |
| `repository` | `string` | No | Source code repository URL. |
| `license` | `string` | No | SPDX license identifier (e.g. `"MIT"`, `"Apache-2.0"`, `"MPL-2.0"`). |
| `tags` | `string[]` | No | Search keywords. |
| `depends` | `string[]` | No | Software IDs that must be installed first. Dependency cycles are invalid and must be rejected. |
| `detect` | `DetectRule[]` | No | Ordered list of rules to check if the software is already installed. |
| `methods` | `InstallMethod[]` | No | Ordered list of ways to install or uninstall the software. |
| `configs` | `ConfigSpec[]` | No | User configuration files or directories suitable for backup/sync. |

## Detection Rules (`detect`)

A software entry is considered installed on a host OS if **any** matching `DetectRule` succeeds.

```json
{
  "os": "linux",
  "kind": "binary",
  "value": "nvim",
  "version_args": ["--version"],
  "version_regex": "NVIM v([0-9.]+)"
}
```

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `os` | `string` | Yes | `"linux"`, `"macos"`, `"windows"`, or `"any"`. |
| `kind` | `string` | Yes | Detection mechanism (see below). |
| `value` | `string` | Yes | Target binary name, path, Flatpak ID, command, etc. |
| `version_args` | `string[]` | No | Optional arguments passed to the binary to print its version. |
| `version_regex` | `string` | No | Optional regex with capture group 1 extracting the version string. |

Supported `kind` values:
- `binary`: Executable present on `PATH` (e.g. `"nvim"`, `"git.exe"`).
- `path`: File or directory exists on disk (`~`, `%APPDATA%`, `%LOCALAPPDATA%`, `%USERPROFILE%` expanded).
- `flatpak`: Installed Flatpak application ID (e.g. `"org.mozilla.firefox"`).
- `snap`: Installed Snap package name.
- `macos_app`: macOS `.app` bundle path (e.g. `"/Applications/Firefox.app"`).
- `command`: Shell command whose exit code `0` indicates installed.

## Install / Uninstall Methods (`methods`)

Each entry in `methods` describes one provider-backed or custom way to install or uninstall the software on a given OS. Consumers pick the first compatible method available on the host (respecting optional `priority`, higher first, or user preference).

```json
{
  "os": "linux",
  "kind": "pacman",
  "package": "neovim"
}
```

Shell installer example with explicit uninstall hook:

```json
{
  "os": "linux",
  "kind": "bash",
  "install_cmd": "curl -sSL https://valk-lang.dev/vman.sh | bash",
  "uninstall_cmd": "rm -rf ~/.vman"
}
```

Windows PowerShell example:

```json
{
  "os": "windows",
  "kind": "powershell",
  "install_cmd": "irm https://valk-lang.dev/vman.ps1 | iex"
}
```

Linux AppImage example:

```json
{
  "os": "linux",
  "kind": "appimage",
  "url": "https://example.com/releases/latest/MyApp-x86_64.AppImage",
  "arch": ["x86_64"]
}
```

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `os` | `string` | Yes | `"linux"`, `"macos"`, `"windows"`, or `"any"`. |
| `kind` | `string` | Yes | Provider or shell runner kind (see below). |
| `package` | `string` | Conditional | Package identifier for package-manager kinds (e.g. `"neovim"`, `"Mozilla.Firefox"`). |
| `remote` | `string` | No | Optional remote/tap/repo name (e.g. `"flathub"`, Homebrew tap, COPR, PPA). |
| `arch` | `string[]` | No | Optional architecture filter (e.g. `["x86_64", "arm64"]`). Omit if all architectures are supported. |
| `url` | `string` | Conditional | Direct download URL for `appimage` methods. |
| `sha256` | `string` | No | Optional 64-character hex SHA-256 checksum for `appimage` downloads. |
| `install_cmd` | `string` | Conditional | Command for shell kinds (`sh`, `bash`, `powershell`, `cmd`), or custom install override. |
| `uninstall_cmd` | `string` | No | Command to uninstall the software. |
| `priority` | `integer` | No | Optional preference weight (default `0`; higher preferred). |

Supported `kind` values:
- Linux system & universal: `pacman`, `aur`, `apt`, `dnf`, `zypper`, `apk`, `flatpak`, `snap`, `nix`, `appimage`
- macOS: `brew`, `brew_cask`
- Windows: `winget`, `scoop`, `choco`
- Shell runners: `sh` (`/bin/sh -c`), `bash` (`bash -c`), `powershell` (`pwsh` / `powershell -NoProfile -Command`), `cmd` (`cmd /C`)

Standard package-manager kinds (`pacman`, `aur`, `apt`, `dnf`, `flatpak`, `brew`, `brew_cask`, `winget`, `scoop`, etc.) have well-known install and uninstall commands so entries only need `package` unless custom behavior is required. For language/ecosystem tools like `vman`, `cargo`, `npm`, or `pipx`, use a shell runner (`sh`, `powershell`, etc.) together with `depends`.

## Dependencies (`depends`)

A software entry may list other catalog IDs in `depends` that must be installed before it:

```json
{
  "id": "jolt",
  "depends": ["vman"]
}
```

Consumers must resolve dependencies topologically (installing missing dependencies first) and reject any unknown dependency ID or dependency cycle (`A -> B -> A` or `A -> A`) as an error.

## Configuration Paths (`configs`)

Lists user-editable config files or directories that tools like `zapps` can sync across machines.

```json
{
  "id": "config",
  "label": "Neovim config (~/.config/nvim)",
  "paths": {
    "linux": "~/.config/nvim",
    "macos": "~/.config/nvim",
    "windows": "%LOCALAPPDATA%\\nvim"
  }
}
```
