from ens import ENS as _ens
from web3 import Web3
from termcolor import cprint
from nubia import command, argument


w3 = Web3()

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
        Converts a ens name to an address
        """

        try:
            cprint("Address of {}: {}".format(value, self.ns.address(value)))
        except Exception as e:
            cprint("Failed to convert {}: {}".format(value, e), "yellow")