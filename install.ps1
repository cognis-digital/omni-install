#requires -version 5
# omni-install — menu installer (Windows, winget).
$items = @(
  @{n="Python";id="Python.Python.3.12"}, @{n="Node.js";id="OpenJS.NodeJS"},
  @{n="Go";id="GoLang.Go"}, @{n="Rust";id="Rustlang.Rustup"}, @{n="Docker";id="Docker.DockerDesktop"},
  @{n="Git";id="Git.Git"}, @{n="GitHub CLI";id="GitHub.cli"}, @{n="Terraform";id="HashiCorp.Terraform"},
  @{n="kubectl";id="Kubernetes.kubectl"}, @{n="Helm";id="Helm.Helm"}, @{n="AWS CLI";id="Amazon.AWSCLI"},
  @{n="Azure CLI";id="Microsoft.AzureCLI"}, @{n="Ollama";id="Ollama.Ollama"}, @{n="Neovim";id="Neovim.Neovim"}
)
Write-Host "== omni-install (winget) ==" -ForegroundColor Cyan
for ($i=0; $i -lt $items.Count; $i++) { Write-Host ("  {0}) {1}" -f ($i+1), $items[$i].n) }
Write-Host "  a) install ALL"
$sel = Read-Host "select (numbers space-separated, or 'a')"
$chosen = if ($sel -eq "a") { $items } else { $sel -split " " | ForEach-Object { $items[[int]$_-1] } }
foreach ($it in $chosen) { Write-Host "Installing $($it.n)..."; winget install --id $it.id -e --accept-source-agreements --accept-package-agreements }
