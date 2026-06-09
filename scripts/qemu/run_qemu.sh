#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT_DIR"

echo "[INFO] Building QEMU firmware"
python3 -m prg32 qemu build-and-flash

echo "[INFO] Starting QEMU screen"
exec python3 -m prg32 qemu launch
