#!/usr/bin/env python3

# Legion - Shayan Eskandari, ConsenSys Diligence

import sys
from nubia import Nubia, Options
from legion_plugin import LegionPlugin
from commands import legion_commands


if __name__ == "__main__":
    plugin = LegionPlugin()
    shell = Nubia(
        name="Legion",
        command_pkgs=legion_commands,
        plugin=plugin,
        options=Options(persistent_history=False),
    )
    sys.exit(shell.run())
