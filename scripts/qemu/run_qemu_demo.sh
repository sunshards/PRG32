#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT_DIR"

echo "[INFO] Building QEMU firmware"
python3 -m prg32 qemu build-and-flash

echo "[INFO] Building demo cartridge"
python3 -m prg32 build-cartridge examples/games/asteroids/graphics/game.S \
  --entry-prefix asteroids_graphics \
  --name asteroids \
  --target qemu \
  --out build-qemu/asteroids.prg32

echo "[INFO] Staging demo cartridge into QEMU flash"
python3 -m prg32 qemu upload build-qemu/asteroids.prg32

echo "[INFO] Starting QEMU screen"
exec python3 -m prg32 qemu launch
