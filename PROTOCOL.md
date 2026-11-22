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
| `detect` | `DetectRule[]` | No | Ordered list of rules to check if the software is already installed. |
| `methods` | `InstallMethod[]` | No | Ordered list of ways to install, update, or uninstall the software. |
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

## Install / Update / Uninstall Methods (`methods`)

Each entry in `methods` describes one provider-backed or custom way to manage the software on a given OS. Consumers pick the first compatible method available on the host (respecting optional `priority`, higher first, or user preference).

```json
{
  "os": "linux",
  "kind": "pacman",
  "package": "neovim"
}
```

Custom script / installer example with explicit update and uninstall hooks:

```json
{
  "os": "linux",
  "kind": "script",
  "install_cmd": "curl -sSL https://valk-lang.dev/vman.sh | bash",
  "update_cmd": "vman self-update",
  "uninstall_cmd": "rm -rf ~/.vman"
}
```

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `os` | `string` | Yes | `"linux"`, `"macos"`, `"windows"`, or `"any"`. |
| `kind` | `string` | Yes | Provider kind (see below). |
| `package` | `string` | Conditional | Package identifier for package-manager kinds (e.g. `"neovim"`, `"Mozilla.Firefox"`, `"github.com/ctxcode/jolt"`). |
| `remote` | `string` | No | Optional remote/tap/repo name (e.g. `"flathub"`, Homebrew tap, COPR, PPA). |
| `arch` | `string[]` | No | Optional architecture filter (e.g. `["x86_64", "arm64"]`). Omit if all architectures are supported. |
| `url` | `string` | Conditional | Direct download URL for `download` / `appimage` methods. |
| `sha256` | `string` | No | Optional SHA-256 checksum for direct downloads. |
| `install_cmd` | `string` | Conditional | Shell command for `script` installs (or custom install override). |
| `update_cmd` | `string` | No | Shell command to update the software (for non-package-manager methods or custom updaters). |
| `uninstall_cmd` | `string` | No | Shell command to uninstall the software. |
| `priority` | `integer` | No | Optional preference weight (default `0`; higher preferred). |

Supported `kind` values:
- Linux system & universal: `pacman`, `aur`, `apt`, `dnf`, `zypper`, `apk`, `flatpak`, `snap`, `nix`, `appimage`
- macOS: `brew`, `brew_cask`
- Windows: `winget`, `scoop`, `choco`
- Language / tool ecosystems: `vman_global`, `cargo`, `npm`, `pipx`
- Generic: `script`, `download`, `github_release`

Standard package-manager kinds (`pacman`, `aur`, `apt`, `dnf`, `flatpak`, `brew`, `brew_cask`, `winget`, `scoop`, `vman_global`, etc.) have well-known install, update, and uninstall commands so entries only need `package` unless custom behavior is required.

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
