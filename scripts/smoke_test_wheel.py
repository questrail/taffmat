# Copyright (c) 2013-2026 The taffmat developers. All rights reserved.
# Project site: https://github.com/questrail/taffmat
# Use of this source code is governed by a MIT-style license that
# can be found in the LICENSE.txt file for the project.
"""Check a built wheel from outside the source tree.

Every other check in this project runs against `src/`, so a packaging mistake
that leaves a module or `py.typed` out of the distribution passes ruff,
pyright, and the whole suite and ships anyway. Run this with the wheel
installed somewhere `src/` cannot be reached:

    uv run --isolated --no-project --with dist/*.whl \
        python scripts/smoke_test_wheel.py 1.0.1

Python puts this file's own directory on `sys.path` rather than the working
directory, so `import taffmat` below can only resolve to the installed wheel.
"""

import argparse
import importlib.metadata
import importlib.resources

import taffmat

# The module carries no __all__, so the public surface is named here. A
# function added to the module belongs in this list.
PUBLIC_NAMES = (
    "change_slope",
    "read_taffmat",
    "write_taffmat",
    "write_taffmat_slice",
)


def main(expected: str) -> None:
    installed = importlib.metadata.version("taffmat")
    if installed != expected:
        raise SystemExit(f"The wheel installed {installed}, expected {expected}")

    for name in PUBLIC_NAMES:
        if not callable(getattr(taffmat, name)):
            raise SystemExit(f"{name} is missing from the wheel")

    if not importlib.resources.files("taffmat").joinpath("py.typed").is_file():
        raise SystemExit("The wheel is missing py.typed")

    print(f"taffmat {installed} imported from {taffmat.__file__}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Check a built taffmat wheel from outside the source tree."
    )
    parser.add_argument(
        "expected_version", help="the version the wheel is expected to install"
    )
    main(parser.parse_args().expected_version)
