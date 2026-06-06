from __future__ import annotations
import argparse
import subprocess
import sys
from pathlib import Path
from prg32.utilities.env_variables import *
import urllib.error
import urllib.request
import json

def run(cmd: list[str], cwd: Path | None = None) -> str:
    try:
        result = subprocess.run(
            cmd,
            cwd=str(cwd) if cwd else None,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except FileNotFoundError as exc:
        raise SystemExit(f"missing tool: {cmd[0]}") from exc
    except subprocess.CalledProcessError as exc:
        sys.stderr.write(exc.stdout)
        sys.stderr.write(exc.stderr)
        raise SystemExit(f"command failed: {' '.join(cmd)}") from exc
    return result.stdout

def parse_nm(text: str) -> dict[str, int]:
    symbols: dict[str, int] = {}
    for line in text.splitlines():
        parts = line.split()
        if len(parts) >= 3:
            try:
                symbols[parts[2]] = int(parts[0], 16)
            except ValueError:
                continue
    return symbols

def parse_nm_sizes(text: str) -> dict[str, int]:
    symbols: dict[str, int] = {}
    for line in text.splitlines():
        parts = line.split()
        if len(parts) >= 4:
            name = parts[-1]
            try:
                size = int(parts[1], 16)
            except ValueError:
                continue
            symbols[name] = size
    return symbols

def runtime_from_elf(path: Path, tool_prefix: str) -> dict:
    nm = parse_nm(run([tool_prefix + "nm", "-g", "--defined-only", str(path)]))
    if "prg32_cart_exec" not in nm:
        raise SystemExit("firmware ELF does not export prg32_cart_exec")
    size_nm = parse_nm_sizes(
        run([tool_prefix + "nm", "-S", "-g", "--defined-only", str(path)])
    )
    missing = [name for name in IMPORT_NAMES if name not in nm]
    if missing:
        raise SystemExit("firmware ELF is missing imports: " + ", ".join(missing))
    ram_size = size_nm.get("prg32_cart_exec")
    if not ram_size:
        ram_size = FALLBACK_CART_RAM_SIZE
        print(
            "warning: could not infer prg32_cart_exec size from ELF symbols; "
            f"using fallback cart RAM size {ram_size} bytes",
            file=sys.stderr,
        )
    return {
        "cart_load_addr": nm["prg32_cart_exec"],
        "cart_ram_size": ram_size,
        "imports": {name: nm[name] for name in IMPORT_NAMES},
    }

def fetch_runtime(url: str) -> dict:
    endpoint = url.rstrip("/") + "/api/runtime"
    try:
        with urllib.request.urlopen(endpoint, timeout=10) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.URLError as exc:
        raise SystemExit(f"failed to read runtime from {endpoint}: {exc}") from exc

def runtime(args: argparse.Namespace) -> None:
    if args.url:
        print(json.dumps(fetch_runtime(args.url), indent=2, sort_keys=True))
    elif args.firmware_elf:
        print(json.dumps(runtime_from_elf(Path(args.firmware_elf), args.tool_prefix),
                         indent=2,
                         sort_keys=True))
    else:
        raise SystemExit("runtime requires --url or --firmware-elf")