""" Cartridge Building for ESP32C6

The cartridge workflow keeps the PRG32 firmware resident on the board. A game
is linked for the firmware's cartridge RAM address and PRG32 API import table,
packed as a .prg32 file, then uploaded over HTTP or staged into QEMU flash.
"""

import urllib.error
import urllib.request
from pathlib import Path
import argparse
from prg32.utilities.env_variables import *

def upload(args: argparse.Namespace) -> None:
    data = Path(args.cartridge).read_bytes()
    endpoint = args.url.rstrip("/") + "/api/games?slot=" + args.slot
    request = urllib.request.Request(
        endpoint,
        data=data,
        method="POST",
        headers={"Content-Type": "application/octet-stream"},
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            print(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", "replace")
        raise SystemExit(f"upload failed: HTTP {exc.code}: {body}") from exc
    except urllib.error.URLError as exc:
        raise SystemExit(f"upload failed: {exc}") from exc
