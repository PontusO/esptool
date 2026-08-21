# SPDX-FileCopyrightText: 2014-2025 Fredrik Ahlberg, Angus Gratton,
# Espressif Systems (Shanghai) CO LTD, other contributors as noted.
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""esptool package entry point.

The command line interface lives in esptool.cli and main() imports it
lazily, so that importing esptool for its Python API needs only pyserial
and intelhex. Importing it eagerly would also require rich_click, click,
rich, markdown-it-py, mdurl and Pygments, none of which an API consumer
touches. See ci/test_api_only_import.sh.
"""

__all__ = [
    "chip_id",
    "detect_chip",
    "dump_mem",
    "elf2image",
    "erase_flash",
    "erase_region",
    "flash_id",
    "attach_flash",
    "get_security_info",
    "image_info",
    "load_ram",
    "merge_bin",
    "read_flash",
    "read_flash_status",
    "read_flash_sfdp",
    "read_mac",
    "read_mem",
    "read_nand_spare",
    "reset_chip",
    "run",
    "run_stub",
    "verify_flash",
    "version",
    "write_flash",
    "write_flash_status",
    "write_mem",
    "write_nand_spare",
]

__version__ = "5.3.1"

from esptool.cmds import (  # noqa: F401
    attach_flash,
    chip_id,
    detect_chip,
    dump_mem,
    elf2image,
    erase_flash,
    erase_region,
    flash_id,
    get_security_info,
    image_info,
    load_ram,
    merge_bin,
    read_flash,
    read_flash_sfdp,
    read_flash_status,
    read_mac,
    read_mem,
    read_nand_spare,
    reset_chip,
    run,
    run_stub,
    verify_flash,
    version,
    write_flash,
    write_flash_status,
    write_mem,
    write_nand_spare,
)

# ESPLoader, FatalError and log are not part of the public __all__ API, but
# three things outside this package still reach for them as esptool.<name>:
# espefuse's own main() type-hints its esp argument as esptool.ESPLoader,
# and that annotation is evaluated eagerly at import time (neither espefuse
# nor espsecure uses "from __future__ import annotations"); both espefuse
# and espsecure catch esptool.FatalError; and esptool.util's own
# check_deprecated_py_suffix() does "from esptool import log" at call time,
# and that helper is used by esptool.cli, espefuse, espsecure and
# esp_rfc2217_server alike. Binding them here costs nothing towards the
# API-only goal: esptool.loader, esptool.util and esptool.logger need
# neither click nor rich, and esptool.cmds (imported above) already pulls
# the first two in as a side effect of its own "from .loader import" /
# "from .util import".
from esptool.loader import ESPLoader  # noqa: F401
from esptool.logger import log  # noqa: F401
from esptool.util import FatalError  # noqa: F401


def main(argv: list[str] | None = None, esp: ESPLoader | None = None):
    """
    Main function for esptool

    argv - Optional override for default arguments parsing (that uses sys.argv),
    can be a list of custom arguments as strings. Arguments and their values
    need to be added as individual items to the list
    e.g. "-b 115200" thus becomes ['-b', '115200'].

    esp - Optional override of the connected device previously
    returned by get_default_connected_device()

    The import of esptool.cli is deferred to this call, so that importing
    the esptool package itself does not require the CLI's dependencies.
    """
    from esptool.cli import main as _cli_main

    return _cli_main(argv, esp)


def _main():
    """Console script entry point (esptool.__init__:_main in setup.py),
    and the target of esptool/__main__.py and the root esptool.py wrapper
    script. Deferred to esptool.cli for the same reason as main() above.
    """
    from esptool.cli import _main as _cli_main

    return _cli_main()


def expand_file_arguments(argv: list[str]) -> list[str]:
    """Used by espefuse's own main() as esptool.expand_file_arguments().
    Deferred to esptool.cli for the same reason as main() above.
    """
    from esptool.cli import expand_file_arguments as _cli_expand_file_arguments

    return _cli_expand_file_arguments(argv)
