#!/usr/bin/env bash
# omni-install — menu installer (Linux/macOS). Detects apt/dnf/pacman/brew.
set -uo pipefail
mgr=""
for m in brew apt-get dnf pacman; do command -v $m >/dev/null && mgr=$m && break; done
[ -z "$mgr" ] && { echo "no supported package manager found"; exit 1; }
inst() { case "$mgr" in
  brew) brew install "$1";; apt-get) sudo apt-get install -y "$1";;
  dnf) sudo dnf install -y "$1";; pacman) sudo pacman -S --noconfirm "$1";; esac; }
items=( "Python:python3" "Node.js:nodejs" "Go:golang" "Docker:docker.io" "Git:git"
        "GitHub CLI:gh" "ripgrep:ripgrep" "fzf:fzf" "Neovim:neovim" "Terraform:terraform"
        "kubectl:kubectl" "Helm:helm" "AWS CLI:awscli" "Azure CLI:azure-cli" )
echo "== omni-install (manager: $mgr) =="
i=1; for it in "${items[@]}"; do echo "  $i) ${it%%:*}"; i=$((i+1)); done
echo "  a) install ALL   q) quit"
read -rp "select (numbers space-separated, or 'a'): " choice
[ "$choice" = "q" ] && exit 0
if [ "$choice" = "a" ]; then for it in "${items[@]}"; do inst "${it##*:}"; done; exit 0; fi
for n in $choice; do it="${items[$((n-1))]}"; [ -n "${it:-}" ] && inst "${it##*:}"; done
