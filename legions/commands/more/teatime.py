import json
import typing
from legions.commands.commands import w3, INFURA_URL, PEER_SAMPLE
from nubia import command, argument
from teatime.scanner import Scanner
from teatime.plugins.context import NodeType
from teatime.plugins.eth1 import *
from termcolor import cprint
from urllib.parse import urlparse

# TODO: Currently no information about severity levels and if intrusive.

# Contains plugins supported by all clients.
SUPPORTED_BY_ALL_CLIENTS = [
    "eth1/AccountCreation",
    "eth1/PeerlistLeak",
    "eth1/MiningStatus",
    "eth1/HashrateStatus",
    "eth1/NetworkListening",
    "eth1/PeerCountStatus",
    "eth1/PeerlistManipulation",
    "eth1/NodeVersion",
    "eth1/TxPoolContent",
    "eth1/NodeSync",
    "eth1/SHA3Consistency",
    "eth1/OpenAccounts",
    "eth1/AccountUnlock",
]

# Maps node types to supported plugins.
SUPPORTED_BY = {
    NodeType.GETH: [
        "eth1/GethAccountImport",
        "eth1/GethDatadir",
        "eth1/GethNodeInfo",
        "eth1/GethStartWebsocket",
        "eth1/GethStopWebsocket",
        "eth1/GethTxPoolInspection",
        "eth1/GethTxPoolStatus",
        "eth1/GethStartRPC",
        "eth1/GethStopRPC",
    ]
    + SUPPORTED_BY_ALL_CLIENTS,
    NodeType.PARITY: [
        "eth1/ParityGasCeiling",
        "eth1/ParityGasFloor",
        "eth1/ParityDevLogs",
        "eth1/ParityChangeCoinbase",
        "eth1/ParityChangeTarget",
        "eth1/ParityChangeExtra",
        "eth1/ParitySyncMode",
        "eth1/ParityDropPeers",
        "eth1/ParityUpgrade",
        "eth1/ParityTxPoolStatistics",
        "eth1/ParityTxCeiling",
        "eth1/ParityMinGasPrice",
    ]
    + SUPPORTED_BY_ALL_CLIENTS,
}


@command
class scan:
    "RPC scans for blockchain nodes powered by teatime"

    # The following variables are used as arguments for some of teatime's
    # plugins.
    infura_url = INFURA_URL

    # Used when importing/creating a new account on the node. The accounts are
    # locked with the specified password.
    password = "legions"

    # Used when importing an exisiting account on the node using a raw key.
    keydata = ""

    # Used when trying to set a new gas ceiling target for mined blocks.
    # Parity defaults to 0x0, see
    # https://openethereum.github.io/wiki/JSONRPC-parity_set-module#parity_setgasceiltarget
    gas_target = 0x0

    # Used when trying to set a new gas floor target for mined blocks.
    # Parity defaults to 0x0, see
    # https://openethereum.github.io/wiki/JSONRPC-parity_set-module#parity_setgasfloortarget
    gas_floor = 0x0

    # Used when trying to set the minimum transaction gas price.
    # Default copied from https://openethereum.github.io/wiki/JSONRPC-parity_set-module#parity_setmingasprice
    gas_price = 0x3E8

    # Used when trying to set the maximum transaction gas.
    # Default copied from https://openethereum.github.io/wiki/JSONRPC-parity_set-module#parity_setmaxtransactiongas
    gas_limit = 0x186A0

    # Used when trying to change the address of the author of the block
    # (the beneficiary to whom the mining rewards were given).
    author = "0x0"

    # Used when trying to change the target chain.
    target_chain = "foundation"  # Ethereum mainnet

    # Used when trying to change the extra data field.
    extra_data = "0x0"

    # Used when trying to change the node's sync mode.
    mode = "active"

    # Used when checking whether the node is mining.
    should_mine = True

    # Used when checking whether the node has a certain hash rate.
    hash_rate = 712000

    # Used when checking whether the node has a certain peer count.
    minimum_peercount = 3

    # Used when trying to unlock accounts.
    wordlist = [""]
    skip_below = 0  # skip accounts below this balance

    # Used when checking SHA3 consistency.
    test_input = ""
    test_output = "0xc5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470"

    # Used when trying to add a peer to a node's peer list.
    test_enode = PEER_SAMPLE

    # Used when checking the node's sync state.
    block_threshold = 10

    # plugin_instantiator is a dict mapping plugin names to a function
    # instantiating and returning them.
    plugin_instantiator = {
        "eth1/AccountCreation": lambda arg=password: AccountCreation(test_password=arg),
        "eth1/TxPoolContent": lambda: TxPoolContent(),
        "eth1/HashrateStatus": lambda arg=hash_rate: HashrateStatus(
            expected_hashrate=arg
        ),
        "eth1/NetworkListening": lambda: NetworkListening(),
        "eth1/NodeSync": lambda arg1=infura_url, arg2=block_threshold: NodeSync(
            infura_url=arg1, block_threshold=arg2
        ),
        "eth1/SHA3Consistency": lambda arg1=test_input, arg2=test_output: SHA3Consistency(
            test_input=arg1, test_output=arg2
        ),
        "eth1/OpenAccounts": lambda arg=infura_url: OpenAccounts(infura_url=arg),
        "eth1/AccountUnlock": lambda arg1=infura_url, arg2=wordlist, arg3=skip_below: AccountUnlock(
            infura_url=arg1, wordlist=arg2, skip_below=arg3
        ),
        "eth1/NodeVersion": lambda: NodeVersion(),
        "eth1/PeerlistLeak": lambda: PeerlistLeak(),
        "eth1/MiningStatus": lambda arg=should_mine: MiningStatus(should_mine=arg),
        "eth1/PeerCountStatus": lambda arg=minimum_peercount: PeerCountStatus(
            minimum_peercount=arg
        ),
        "eth1/PeerlistManipulation": lambda arg=test_enode: PeerlistManipulation(
            test_enode=arg
        ),
        # Geth
        "eth1/GethNodeInfo": lambda: GethNodeInfo(),
        "eth1/GethAccountImport": lambda arg1=keydata, arg2=password: GethAccountImport(
            keydata=arg1, password=arg2
        ),
        "eth1/GethStartWebsocket": lambda: GethStartWebsocket(),
        "eth1/GethStopWebsocket": lambda: GethStopWebsocket(),
        "eth1/GethTxPoolInspection": lambda: GethTxPoolInspection(),
        "eth1/GethTxPoolStatus": lambda: GethTxPoolStatus(),
        "eth1/GethStartRPC": lambda: GethStartRPC(),
        "eth1/GethStopRPC": lambda: GethStopRPC(),
        "eth1/GethDatadir": lambda: GethDatadir(),
        # Parity
        "eth1/ParityGasCeiling": lambda arg=gas_target: ParityGasCeiling(
            gas_target=arg
        ),
        "eth1/ParityDevLogs": lambda: ParityDevLogs(),
        "eth1/ParityGasFloor": lambda arg=gas_floor: ParityGasFloor(gas_floor=arg),
        "eth1/ParityUpgrade": lambda: ParityUpgrade(),
        "eth1/ParityTxPoolStatistics": lambda: ParityTxPoolStatistics(),
        "eth1/ParityTxCeiling": lambda arg=gas_limit: ParityTxCeiling(gas_limit=arg),
        "eth1/ParityMinGasPrice": lambda arg=gas_price: ParityMinGasPrice(
            gas_price=arg
        ),
        "eth1/ParitySyncMode": lambda arg=mode: ParitySyncMode(mode=arg),
        "eth1/ParityChangeCoinbase": lambda arg=author: ParityChangeCoinbase(
            author=arg
        ),
        "eth1/ParityChangeTarget": lambda arg=target_chain: ParityChangeTarget(
            target_chain=arg
        ),
        "eth1/ParityChangeExtra": lambda arg=extra_data: ParityChangeExtra(
            extra_data=arg
        ),
        "eth1/ParityDropPeers": lambda: ParityDropPeers(),
    }

    # Contains plugin names added with the `add` command.
    added_plugins = set()

    def __init__(self) -> None:
        # Set node_type.
        if "geth" in w3.clientVersion.lower():
            self.node_type = NodeType.GETH
        elif "parity" in w3.clientVersion.lower():
            self.node_type = NodeType.PARITY
        else:
            cprint("Unsupported node type", "red")

        # Break w3.node_uri in prefix, host and port as expected by teatime.
        url = urlparse(w3.node_uri)
        self.prefix = url.scheme + "://"

        if ":" in url.netloc:
            end = url.netloc.index(":")  # Exclude port information
            self.host = url.netloc[:end] + url.path
        else:
            self.host = url.netloc + url.path

        if url.port is None:
            self.port = 8545  # Default port
        else:
            self.port = url.port

    @command("execute")
    def execute(self) -> str:
        """
        Execute RPC scanner
        """
        if not self.added_plugins:
            cprint("No plugins selected", "red")
            return

        # Create a list containing the instantiated plugins.
        instantiated_plugins = [
            self.plugin_instantiator[p]() for p in self.added_plugins
        ]

        # Run a new scanner.
        report = Scanner(
            self.host, self.port, self.node_type, instantiated_plugins, self.prefix
        ).run()

        # Print report.
        out = json.dumps(report.to_dict(), indent=2)
        cprint("Scanreport:", "yellow")
        cprint("{}".format(out))

    # Add commands

    @command("add")
    @argument(
        "plugin", description="add plugin to RPC scanner", choices=plugin_instantiator
    )
    def add(self, plugin: str) -> None:
        """
        Add plugin to RPC scanner
        """
        if plugin in SUPPORTED_BY[self.node_type]:
            self.added_plugins.add(plugin)
        else:
            cprint(
                "{} either not supported by current node or not existing".format(
                    plugin
                ),
                "yellow",
            )

    # If argument is type list we can not define `choices`, making it
    # unusable for interactive mode.
    @command("add-list")
    @argument("plugins", description="add plugin(s) to RPC scanner")
    def add_list(self, plugins: typing.List[str]) -> None:
        """
        Add plugin(s) to RPC scanner
        """
        for plugin in plugins:
            if plugin in SUPPORTED_BY[self.node_type]:
                self.added_plugins.add(plugin)
            else:
                cprint(
                    "{} either not supported by current node or not existing".format(
                        plugin
                    ),
                    "yellow",
                )

    @command("rm")
    @argument(
        "plugin",
        description="remove plugin from RPC scanner",
        choices=plugin_instantiator,
    )
    def rm(self, plugin: str) -> None:
        """
        Remove plugin from RPC scanner
        """
        self.added_plugins.discard(plugin)

    # List commands

    @command("list-all")
    def list_all(self) -> None:
        """
        List all plugins
        """
        geth = set(SUPPORTED_BY[NodeType.GETH])
        parity = set(SUPPORTED_BY[NodeType.PARITY])
        plugins = geth.union(parity)

        cprint("Plugins:", "yellow")
        for plugin in plugins:
            cprint("+ " + plugin)

    @command("list-selected")
    def list_selected(self) -> None:
        """
        List selected plugins
        """
        if not self.added_plugins:
            cprint("No plugins selected", "yellow")
            return

        cprint("Plugins selected:", "yellow")
        for plugin in self.added_plugins:
            cprint("+ " + plugin)

    @command("list-geth")
    def list_geth(self) -> None:
        """
        List plugins supported by Geth
        """
        cprint("Plugins supported by Geth:", "yellow")
        for plugin in SUPPORTED_BY[NodeType.GETH]:
            cprint("+ " + plugin)

    @command("list-parity")
    def list_parity(self) -> None:
        """
        List plugins supported by Parity
        """
        cprint("Plugins supported by Parity:", "yellow")
        for plugin in SUPPORTED_BY[NodeType.PARITY]:
            cprint("+ " + plugin)
