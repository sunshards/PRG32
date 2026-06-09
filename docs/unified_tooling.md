# PRG32 Unified Tooling Guide

The new PRG32 Python-based toolchain (`python3 -m prg32`) drastically simplifies the workflow for both physical ESP32-C6 hardware and the QEMU emulator. It replaces the long and complex `idf.py` commands and platform-specific shell scripts (like `qemu.sh` or `qemu.ps1`) with a single, cross-platform interface.

This guide covers how to use the `prg32` module to perform the fundamental tasks: launching the firmware on ESP32-C6, launching QEMU, building cartridges, and uploading cartridges.

## 1. Preparing the Firmware

Instead of manually running `idf.py set-target`, `idf.py build`, and `idf.py flash monitor` with different configuration files, the `prg32` tool handles the entire pipeline.

### For ESP32-C6 (Physical Hardware)
To build and flash the resident firmware to a connected ESP32-C6 board:

```bash
python3 -m prg32 esp32c6 build-and-flash
```

### For QEMU (Emulator)
To build the firmware for the QEMU emulator target and generate the virtual flash image:

```bash
python3 -m prg32 qemu build-and-flash
```

Once built and flashed, you can launch the QEMU graphical emulator with:

```bash
python3 -m prg32 qemu launch
```

> [!NOTE]
> Because `python3 -m prg32` is cross-platform, you no longer need to use `scripts/qemu/build_qemu.sh` (macOS/Linux) or `tools/qemu.ps1` (Windows). The `launch` command works consistently across all operating systems.

## 2. Building Cartridges

The process for compiling games into `.prg32` cartridges has been streamlined. You no longer need to manually find and pass the correct `--firmware-elf` path unless you are doing advanced development. You can simply specify the `--target`.

### Building for ESP32-C6
```bash
python3 -m prg32 build-cartridge examples/games/asteroids/graphics/game.S \
  --name asteroids \
  --entry-prefix asteroids_graphics \
  --target esp32c6 \
  --out build-esp32c6/asteroids.prg32
```

### Building for QEMU
```bash
python3 -m prg32 build-cartridge examples/games/asteroids/graphics/game.S \
  --name asteroids \
  --entry-prefix asteroids_graphics \
  --target qemu \
  --out build-qemu/asteroids.prg32
```

## 3. Uploading and Running Cartridges

Uploading cartridges to hardware or staging them into QEMU is now handled by dedicated subcommands in the `esp32c6` and `qemu` task groups.

### Uploading to ESP32-C6
To upload a cartridge over HTTP to a running ESP32-C6 board and immediately run it:

```bash
python3 -m prg32 esp32c6 upload-and-run build-esp32c6/asteroids.prg32
```

Other available ESP32-C6 commands include:
- `upload`: Upload a cartridge over HTTP without automatically running it.
- `run`: Run an already uploaded cartridge.
- `switch-cartridge`: Switch to a different cartridge on the board.

### Uploading to QEMU
To stage a cartridge into the QEMU virtual flash image (make sure QEMU is currently stopped):

```bash
python3 -m prg32 qemu upload build-qemu/asteroids.prg32
```

After staging the cartridge, you can launch the emulator to play the game:

```bash
python3 -m prg32 qemu launch
```

## 4. Additional Utilities

The new toolchain also provides handy utilities to help with debugging and diagnosing environment issues.

### Doctor
To verify that your local toolchain (including ESP-IDF and the RISC-V compiler) is installed and configured correctly, run:

```bash
python3 -m prg32 doctor
```

### Runtime
To query runtime information directly from an active environment, either via HTTP on a real board or by reading a firmware ELF file, run:

```bash
python3 -m prg32 runtime
```

This will print the loaded cartridge load address, ABI version, RAM size, and PRG32 API import addresses.

## 5. CartridgeStore and Metadata Tooling

The unified tooling now includes a dedicated `store` subcommand to handle all metadata appending and CartridgeStore integrations. This replaces the old `python3 -m prg32` standalone metadata commands.

### Metadata Management
You can append the required `prg32-metadata-1.0` JSON and assets to a compiled cartridge, or inspect an existing cartridge's metadata:

```bash
# Attach metadata and assets to a built cartridge
python3 -m prg32 store attach-metadata build-esp32c6/asteroids.prg32 \
  --out build-esp32c6/asteroids_meta.prg32 \
  --metadata metadata.json \
  --icon icon.png

# Inspect metadata trailer
python3 -m prg32 store inspect-metadata build-esp32c6/asteroids_meta.prg32
```

### CartridgeStore Discovery and Downloading
To browse or download games from a local or remote CartridgeStore:

```bash
# Discover local CartridgeStore instances via mDNS
python3 -m prg32 store discover --timeout 3

# List available cartridges on a specific store
python3 -m prg32 store list --store-url http://192.168.1.100:5080

# Download a specific game
python3 -m prg32 store download org.prg32.asteroids \
  --store-url http://192.168.1.100:5080 \
  --architecture esp32c6 \
  --out downloaded_asteroids.prg32
```

### Publishing
Publishing bundles cartridges and their metadata together and uploads them to a store:

```bash
# Build, pack, and publish directly
python3 -m prg32 store publish examples/games/asteroids/graphics/game.S \
  --name asteroids \
  --entry-prefix asteroids_graphics \
  --target esp32c6 \
  --store-url http://192.168.1.100:5080

# Alternatively, pack a zip bundle and publish it
python3 -m prg32 store pack-bundle --manifest manifest.json --out bundle.zip
python3 -m prg32 store publish-bundle bundle.zip --store-url http://192.168.1.100:5080
```

## Summary of Commands

Here is a quick reference table of the old vs new workflows:

| Task | Old Command(s) | New Unified Command |
|---|---|---|
| **Build & Flash ESP32-C6** | `idf.py -B build-esp32c6 ... build flash monitor` | `python3 -m prg32 esp32c6 build-and-flash` |
| **Build QEMU Firmware** | `python3 -m prg32 qemu build-and-flash` (or `idf.py`) | `python3 -m prg32 qemu build-and-flash` |
| **Launch QEMU** | `python3 -m prg32 qemu launch` (or `tools/qemu.ps1`) | `python3 -m prg32 qemu launch` |
| **Build Cartridge** | `python3 -m prg32 build-cartridge ... --firmware-elf ...` | `python3 -m prg32 build-cartridge ... --target ...` |
| **Upload to ESP32-C6** | `python3 -m prg32 esp32c6 upload-and-run ...` | `python3 -m prg32 esp32c6 upload-and-run ...` |
| **Stage in QEMU** | `python3 -m prg32 qemu upload ...` | `python3 -m prg32 qemu upload ...` |

Using the `prg32` Python module abstracts the ESP-IDF and operating system differences away, providing a consistent experience for all users.
