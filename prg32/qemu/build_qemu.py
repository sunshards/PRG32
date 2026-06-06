#!/usr/bin/env python3

import subprocess
import argparse
from prg32.utilities.logging import *
from prg32.utilities.env_variables import QEMU_BUILD_DIR as BUILD_DIR

def build_qemu(args: argparse.Namespace):
    step("Configuring QEMU target (esp32c3)")
    subprocess.check_call(["idf.py", "-B", BUILD_DIR, "-D", "SDKCONFIG=build-qemu/sdkconfig", "-D", "SDKCONFIG_DEFAULTS=sdkconfig.defaults.qemu", "set-target", "esp32c3"])
    step("Building QEMU firmware and flash_image")
    subprocess.check_call(["idf.py", "-B", BUILD_DIR, "-D", "SDKCONFIG=build-qemu/sdkconfig", "-D", "SDKCONFIG_DEFAULTS=sdkconfig.defaults.qemu", "qemu", "--graphics", "monitor"])
    # Verify
    if not (Path := __import__('pathlib').Path)(f"{BUILD_DIR}/PRG32.elf").exists():
        die(f"Missing {BUILD_DIR}/PRG32.elf after build.")
    log_info("Firmware build ready")