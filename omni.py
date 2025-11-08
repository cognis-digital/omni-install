#!/usr/bin/env python3
"""omni-install — cross-platform menu installer (stdlib only)."""
import platform, shutil, subprocess, sys
CATALOG = {
    "Python": {"apt":"python3","brew":"python","winget":"Python.Python.3.12"},
    "Node.js": {"apt":"nodejs","brew":"node","winget":"OpenJS.NodeJS"},
    "Go": {"apt":"golang","brew":"go","winget":"GoLang.Go"},
    "Docker": {"apt":"docker.io","winget":"Docker.DockerDesktop"},
    "Git": {"apt":"git","brew":"git","winget":"Git.Git"},
    "GitHub CLI": {"apt":"gh","brew":"gh","winget":"GitHub.cli"},
    "Terraform": {"apt":"terraform","brew":"terraform","winget":"HashiCorp.Terraform"},
    "kubectl": {"brew":"kubernetes-cli","winget":"Kubernetes.kubectl"},
    "Ollama": {"winget":"Ollama.Ollama"},
}
def mgr():
    if platform.system()=="Windows": return "winget"
    if shutil.which("brew"): return "brew"
    if shutil.which("apt-get"): return "apt"
    return ""
def install(name, m):
    pid = CATALOG[name].get(m)
    if not pid: print(f"  (no {m} package for {name})"); return
    if m=="winget": subprocess.run(["winget","install","--id",pid,"-e","--accept-source-agreements","--accept-package-agreements"])
    elif m=="brew": subprocess.run(["brew","install",pid])
    elif m=="apt": subprocess.run(["sudo","apt-get","install","-y",pid])
def main():
    m = mgr()
    if not m: print("no supported package manager"); return 1
    names = list(CATALOG)
    print(f"== omni-install ({m}) ==")
    for i,n in enumerate(names,1): print(f"  {i}) {n}")
    print("  a) ALL")
    sel = input("select: ").strip()
    chosen = names if sel=="a" else [names[int(x)-1] for x in sel.split() if x.isdigit()]
    for n in chosen: print(f"Installing {n}..."); install(n, m)
    return 0
if __name__=="__main__": sys.exit(main())
