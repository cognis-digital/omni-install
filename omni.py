#!/usr/bin/env python3
"""omni-install — cross-platform menu installer (stdlib only).

Subcommands:
    python omni.py            Quick package-manager menu (languages/clouds/tools).
    python omni.py setup      Launch the guided Cognis setup wizard (recommended
                              for first-timers — a numbered, beginner-friendly
                              menu that adapts to your familiarity level).

`setup` forwards any extra flags to the wizard, e.g.:
    python omni.py setup --dry-run
    python omni.py setup --manifest https://raw.githubusercontent.com/cognis-digital/cognis-arsenal/master/MANIFEST.json
"""
import os
import platform
import shutil
import subprocess
import sys


def run_setup(argv):
    """Delegate to the canonical guided wizard (cognis_setup.py, stdlib only)."""
    here = os.path.dirname(os.path.abspath(__file__))
    if here not in sys.path:
        sys.path.insert(0, here)
    try:
        import cognis_setup
    except Exception as exc:  # pragma: no cover - defensive
        print(f"could not load the setup wizard: {exc}", file=sys.stderr)
        return 1
    return cognis_setup.main(argv)


CATALOG = {
    "Python": {"apt": "python3", "brew": "python", "winget": "Python.Python.3.12"},
    "Node.js": {"apt": "nodejs", "brew": "node", "winget": "OpenJS.NodeJS"},
    "Go": {"apt": "golang", "brew": "go", "winget": "GoLang.Go"},
    "Docker": {"apt": "docker.io", "winget": "Docker.DockerDesktop"},
    "Git": {"apt": "git", "brew": "git", "winget": "Git.Git"},
    "GitHub CLI": {"apt": "gh", "brew": "gh", "winget": "GitHub.cli"},
    "Terraform": {"apt": "terraform", "brew": "terraform", "winget": "HashiCorp.Terraform"},
    "kubectl": {"brew": "kubernetes-cli", "winget": "Kubernetes.kubectl"},
    "Ollama": {"winget": "Ollama.Ollama"},
}


def mgr():
    if platform.system() == "Windows":
        return "winget"
    if shutil.which("brew"):
        return "brew"
    if shutil.which("apt-get"):
        return "apt"
    return ""


def install(name, m):
    if name not in CATALOG:
        print(f"  (unknown tool: {name})", file=sys.stderr)
        return
    pid = CATALOG[name].get(m)
    if not pid:
        print(f"  (no {m} package for {name})")
        return
    if m == "winget":
        subprocess.run(
            ["winget", "install", "--id", pid, "-e",
             "--accept-source-agreements", "--accept-package-agreements"]
        )
    elif m == "brew":
        subprocess.run(["brew", "install", pid])
    elif m == "apt":
        subprocess.run(["sudo", "apt-get", "install", "-y", pid])


def main():
    m = mgr()
    if not m:
        print("no supported package manager found (winget/brew/apt-get)", file=sys.stderr)
        return 1
    names = list(CATALOG)
    print(f"== omni-install ({m}) ==")
    for i, n in enumerate(names, 1):
        print(f"  {i}) {n}")
    print("  a) ALL")
    try:
        sel = input("select: ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\nAborted.", file=sys.stderr)
        return 1

    if sel == "a":
        chosen = names
    else:
        chosen = []
        for x in sel.split():
            if not x.isdigit():
                continue
            idx = int(x) - 1
            if 0 <= idx < len(names):
                chosen.append(names[idx])
            else:
                print(f"  (skipping out-of-range selection: {x})", file=sys.stderr)

    if not chosen:
        print("  Nothing to install.", file=sys.stderr)
        return 1

    for n in chosen:
        print(f"Installing {n}...")
        install(n, m)
    return 0


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "setup":
        sys.exit(run_setup(sys.argv[2:]))
    sys.exit(main())
