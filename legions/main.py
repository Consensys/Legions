import sys

from nubia import Nubia, Options
from legions.plugin import LegionPlugin
from legions import commands


def main():
    plugin = LegionPlugin()
    shell = Nubia(
        name="legions",
        command_pkgs=commands,
        plugin=plugin,
        options=Options(persistent_history=True),
    )
    sys.exit(shell.run())
