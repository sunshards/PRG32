#!/usr/bin/env python3
import os
from prg32.utilities.env_variables import QEMU_IMAGE, QEMU_EFUSE
from prg32.utilities.logging import *
import argparse

def launch_qemu(args: argparse.Namespace):
    log_info("Launching QEMU")
    log_info("Press Ctrl + ] to exit")
    cmd = [
        "qemu-system-riscv32",
        "-M",
        "esp32c3",
        "-m",
        "4M",
        "-drive",
        f"file={QEMU_IMAGE},if=mtd,format=raw",
        "-drive",
        f"file={QEMU_EFUSE},if=none,format=raw,id=efuse",
        "-global",
        "driver=nvram.esp32c3.efuse,property=drive,value=efuse",
        "-global",
        "driver=timer.esp32c3.timg,property=wdt_disable,value=true",
        "-nic",
        "user,model=open_eth",
        "-display",
        "sdl",
        "-serial",
        "mon:stdio",
    ]
    os.execvp(cmd[0], cmd)
