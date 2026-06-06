#!/usr/bin/env python3
import subprocess
from pathlib import Path


def main():
    root = Path(__file__).resolve().parents[2]
    subprocess.check_call(["idf.py", "set-target", "esp32c6"], cwd=str(root))
    subprocess.check_call(["idf.py", "build"], cwd=str(root))
    subprocess.check_call(["idf.py", "flash", "monitor"], cwd=str(root))


if __name__ == "__main__":
    main()
