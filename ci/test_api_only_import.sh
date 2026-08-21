#!/usr/bin/env bash
# Prove that importing esptool for its Python API needs only pyserial and
# intelhex, not the command line stack (rich_click and its five dependencies).
#
# A library consumer of detect_chip() and run_stub() should not have to install
# a terminal formatter. arduino-pico ships this fork as a submodule and puts it
# on sys.path next to its own vendored pyserial, so anything beyond that would
# have to be vendored too.
set -euo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
venv="$(mktemp -d)/api-only"
trap 'rm -rf "$(dirname "$venv")"' EXIT

python3 -m venv "$venv"
"$venv/bin/pip" install -q pyserial intelhex

PYTHONPATH="$here" "$venv/bin/python3" - <<'PY'
import esptool
import esptool.reset
import esptool.logger

missing = [n for n in esptool.__all__ if not hasattr(esptool, n)]
assert not missing, "names in __all__ not exported: %r" % missing
assert hasattr(esptool.reset, "RP2040Reset"), "RP2040Reset missing: not the iLabs fork"
assert hasattr(esptool.logger, "EsptoolLogger"), "EsptoolLogger missing"
assert callable(esptool.main), "main() must survive the CLI split"

import sys
for cli_only in ("rich_click", "click", "rich", "pygments"):
    assert cli_only not in sys.modules, \
        "%s was imported: the CLI is still eager" % cli_only

print("API-only import OK, esptool %s" % esptool.__version__)
PY
