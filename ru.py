#!/usr/bin/env python3
import os
import sys
import subprocess
from pathlib import Path

# Detect OS
is_windows = "windows" in sys.platform.lower()
EXE_EXT = ".exe" if is_windows else ""

# CPU count
import multiprocessing
cpu_count = multiprocessing.cpu_count()

# Rust targets for Windows
win_targets = {
    "x86_64": "x86_64-pc-windows-gnu",
    "x86": "i686-pc-windows-gnu"
}

# Path to native/src (where magiskboot Cargo.toml is)
native_src = Path("native", "src")

def run_cargo(cmds, env=None):
    """Run cargo commands"""
    return subprocess.run(["cargo", *cmds], cwd=native_src, env=env)

def build_magiskboot_windows(release=True):
    """Build magiskboot for Windows 32-bit and 64-bit"""
    profile = "--release" if release else ""
    for arch, target in win_targets.items():
        print(f"Building magiskboot for {arch} ({target})...")
        cmd = ["build", "--bin", "magiskboot", "--target", target]
        if release:
            cmd.append("--release")
        proc = run_cargo(cmd)
        if proc.returncode != 0:
            sys.exit(f"Build failed for {arch} ({target})!")

        # Copy the binary to out/ directory
        target_dir = native_src / "target" / target / ("release" if release else "debug")
        out_dir = Path("out") / "windows" / arch
        out_dir.mkdir(parents=True, exist_ok=True)
        binary_name = f"magiskboot{EXE_EXT}"
        src = target_dir / binary_name
        dst = out_dir / binary_name
        print(f"Copying {src} -> {dst}")
        dst.write_bytes(src.read_bytes())

def main():
    build_magiskboot_windows()

if __name__ == "__main__":
    main()
