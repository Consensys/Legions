#!/usr/bin/env python3

# Legion - Shayan Eskandari, ConsenSys Diligence

import sys
from nubia import Nubia, Options
from legion.plugin import LegionPlugin
from legion import commands


def main():
    plugin = LegionPlugin()
    shell = Nubia(
        name="legion",
        command_pkgs=commands,
        plugin=plugin,
        options=Options(persistent_history=True),
    )
    sys.exit(shell.run())


if __name__ == "__main__":
    main()