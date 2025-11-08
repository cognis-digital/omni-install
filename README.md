<div align="center">

# omni-install

### One menu to install every language, cloud CLI, container, and AI tool — on Linux, macOS, or Windows.

[![License: COCL 1.0](https://img.shields.io/badge/License-COCL%201.0-2b6cb0.svg)](LICENSE) ![Cross-platform](https://img.shields.io/badge/Linux%20%C2%B7%20macOS%20%C2%B7%20Windows-supported-2b6cb0) [![Suite](https://img.shields.io/badge/Cognis-Neural%20Suite-6b46c1.svg)](https://github.com/cognis-digital/cognis-neural-suite)

</div>

Pick what you want from a menu; it dispatches to the right package manager (apt/dnf/pacman/brew/winget).

```bash
# Linux / macOS
bash install.sh
# Python TUI (any OS)
python omni.py
```
```powershell
# Windows
powershell -ExecutionPolicy Bypass -File install.ps1
```

Edit **[catalog.yaml](catalog.yaml)** to add tools. Want a whole prebaked image instead? See
**[cognis-devbox](https://github.com/cognis-digital/cognis-devbox)**.

## License
COCL v1.0 — see [LICENSE](LICENSE).
