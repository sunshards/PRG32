#!/usr/bin/env python3
"""Main entry for PRG32"""

from __future__ import annotations
import argparse
import sys
from prg32.utilities.env_variables import *
from prg32.qemu.upload_qemu import upload_qemu
from prg32.utilities.environment_check import doctor
from prg32.cartridge.build_cartridge import build_cartridge_cli
from prg32.utilities.runtime_handler import runtime
from prg32.esp32c6.upload_esp32c6 import upload
from prg32.qemu.launch_qemu import launch_qemu
from prg32.qemu.build_qemu import build_qemu

def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tool-prefix", default="riscv32-esp-elf-")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("runtime", help="print runtime linker information")
    p.add_argument("--url")
    p.add_argument("--firmware-elf")
    p.set_defaults(func=runtime)

    p = sub.add_parser("build-cartridge", help="build a .prg32 cartridge with options from assembly or C")
    p.add_argument("source")
    p.add_argument("--out", required=True)
    p.add_argument("--name", required=True)
    p.add_argument("--entry-prefix", required=True)
    p.add_argument("--target", choices=["esp32c6", "qemu"], default="esp32c6", help="Target environment")
    p.add_argument("--runtime-url")
    p.add_argument("--firmware-elf")
    p.add_argument("--build-dir")
    p.add_argument(
        "--audio-block",
        help="optional PRG32 AUDIO block produced by tools/prg32audio_pack.py",
    )
    p.add_argument("--march", default="rv32imc_zicsr_zifencei")
    p.add_argument("--mabi", default="ilp32")
    p.set_defaults(func=build_cartridge_cli)

    p = sub.add_parser("doctor", help="check local toolchain prerequisites")
    p.add_argument("--partitions", default=str(DEFAULT_PARTITION_TABLE))
    p.add_argument("--slot", default=DEFAULT_CART_SLOT)
    p.add_argument(
        "--host-only",
        action="store_true",
        help="skip ESP-IDF and RISC-V toolchain checks for CI/unit-test hosts",
    )
    p.set_defaults(func=doctor)

    # ==========================================
    # 'esp32c6' Subcommand Menu
    # ==========================================
    
    esp32c6_p = sub.add_parser("esp32c6", help="ESP32C6 SoC tasks")
    # Add a subparser tracker specifically for sub-commands of qemu
    esp32c6_sub = esp32c6_p.add_subparsers(dest="sub_cmd", required=True)

    p = esp32c6_sub.add_parser("upload", help="upload a cartridge to the ESP32C6 SoC over HTTP")
    p.add_argument("cartridge")
    p.add_argument("--url", default="http://192.168.4.1")
    p.add_argument("--slot", default=DEFAULT_CART_SLOT)
    p.set_defaults(func=upload)

    # ==========================================
    # 'qemu' Subcommand Menu
    # ==========================================
    qemu_p = sub.add_parser("qemu", help="QEMU emulator tasks")
    # Add a subparser tracker specifically for sub-commands of qemu
    qemu_sub = qemu_p.add_subparsers(dest="sub_cmd", required=True)

    p =  qemu_sub.add_parser("build", help="build QEMU")
    p.set_defaults(func=build_qemu)

    p = qemu_sub.add_parser("launch", help="launch the QEMU emulator environment")
    p.set_defaults(func=launch_qemu)

    p = qemu_sub.add_parser("upload", 
        help="stage a cartridge into QEMU flash",
        usage="%(prog)s CARTRIDGE [--flash FLASH_IMAGE] [--partitions PARTITION_TABLE] [--slot SLOT]"
    )
    p.add_argument("cartridge")
    p.add_argument("--flash", default=QEMU_IMAGE)
    p.add_argument("--partitions", default=str(DEFAULT_PARTITION_TABLE))
    p.add_argument("--slot", default=DEFAULT_CART_SLOT)
    p.set_defaults(func=upload_qemu)

    args = parser.parse_args(argv)
    args.func(args)
    return 0

if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
