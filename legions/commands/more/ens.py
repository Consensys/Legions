from ens import ENS as _ens
from web3 import Web3
from termcolor import cprint
from nubia import command, argument
from legions.commands.commands import w3


@command
class ens:
    "Ethereum name system"

    def __init__(self) -> None:
        self.ns = _ens.fromWeb3(w3)
        pass

    @command("toName")
    @argument("value", description="address to be converted to a name")
    def toName(self, value: str) -> str:
        """
        Converts an address to a ens name
        """

        try:
            cprint("Name of {}: {}".format(value, self.ns.name(value)))
        except Exception as e:
            cprint("Failed to convert {}: {}".format(value, e), "yellow")

    @command("toAddress")
    @argument("value", description="name to be converted to an address")
    def toAddress(self, value: str) -> str:
        """
        Converts a ENS name to an address
        """

        try:
            cprint("Address of {}: {}".format(value, self.ns.address(value)))
        except Exception as e:
            cprint("Failed to convert {}: {}".format(value, e), "yellow")

    @command("info")
    @argument("name", description="name to get information about")
    def info(self, name: str) -> str:
        """
        Get info about an ENS name
        """

        cprint("Information about '{}'".format(name))
        cprint("Valid name: {}".format(self.ns.is_valid_name(name)))

        if self.ns.is_valid_name(name):
            cprint("Namehash: {}".format(self.ns.namehash(name).hex()))

            resolver = self.ns.resolver(name)
            if resolver is not None:
                cprint("Resolver: {}".format(resolver.address))
                cprint("Owner: {}".format(self.ns.owner(name)))
            else:
                cprint("Is not registered")
