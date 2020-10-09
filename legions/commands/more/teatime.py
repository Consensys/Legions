from teatime.scanner import Scanner
from teatime.plugins.context import NodeType
from teatime.plugins.eth1 import *
from termcolor import cprint
from nubia import command, argument
from legions.commands.commands import w3
from typing import List
from urllib.parse import urlparse

# TODO: Currently no information about severity levels and if intrusive.
#       How to include them? UX could be overwhelming with to many infos.
# TODO: Should there be some default added plugins?

# Docs
#
# TODO: Update README with new commands.

# Plugin variables
#
# TODO: Maybe add a config file defining plugin variables?
#       A `set <var>` would be possible but propably only for a few vars,
#       i.e. the ones which are actually reset from time to time.
# TODO: Find reasonable default values for plugin variables.

# Output
#
# TODO: teatime logs itself, which looks weird in console. Fix!
# TODO: Print scanreport in a nice way
# TODO: Print info text when module invoked? What about help text?
# TODO: Add a `list` command to list selected plugins.

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

    # This variables are used as arguments for some teatime plugins.
    # TODO: They should be instantiated with reasonable defaults.
    password = "default"
    gasceiling = "default"
    gasfloor = "default"
    gas_price = "default"
    gas_limit = "default"
    author = "default"
    target_chain = "default"
    extra_data = "default"
    mode = "default"
    should_mine = True
    hash_rate = 0
    minimum_peercount = 0
    infura_url = "default"  # TODO: set from w3?
    word_list = ["default", "default"]
    skip_below = 0
    test_input = "default"
    test_output = "default"
    test_enode = ""
    block_threshold = 10

    # pluginInstantiator is a dict mapping plugin names to a function
    # instantiating and returning them.
    pluginInstantiator = {
        "eth1/AccountCreation": lambda arg=password: AccountCreation(arg),
        "eth1/TxPoolContent": lambda: TxPoolContent(),
        "eth1/HashrateStatus": lambda arg=hash_rate: HashrateStatus(arg),
        "eth1/NetworkListening": lambda: NetworkListening(),
        "eth1/NodeSync": lambda arg1=infura_url, arg2=block_threshold: NodeSync(
            arg1, arg2
        ),
        "eth1/SHA3Consistency": lambda arg1=test_input, arg2=test_output: SHA3Consistency(
            arg1, arg2
        ),
        "eth1/OpenAccounts": lambda arg=infura_url: OpenAccounts(arg),
        "eth1/AccountUnlock": lambda arg1=infura_url, arg2=word_list, arg3=skip_below: AccountUnlock(
            arg1, arg2, arg3
        ),
        # TODO: Expects optional Geth and Parity url, defaulted by teatime.
        #       Should add args anyway?
        "eth1/NodeVersion": lambda: NodeVersion(),
        "eth1/PeerlistLeak": lambda: PeerlistLeak(),
        "eth1/MiningStatus": lambda arg=should_mine: MiningStatus(arg),
        "eth1/PeerCountStatus": lambda arg=minimum_peercount: PeerCountStatus(arg),
        "eth1/PeerlistManipulation": lambda arg=test_enode: PeerlistManipulation(arg),
        # Geth
        "eth1/GethNodeInfo": lambda: GethNodeInfo(),
        # TODO: PR#12 in teatime adds `Geth` as prefix to class name.
        "eth1/GethAccountImport": lambda arg=password: AccountImport(arg),
        "eth1/GethStartWebsocket": lambda: GethStartWebsocket(),
        "eth1/GethStopWebsocket": lambda: GethStopWebsocket(),
        "eth1/GethTxPoolInspection": lambda: GethTxPoolInspection(),
        "eth1/GethTxPoolStatus": lambda: GethTxPoolStatus(),
        "eth1/GethStartRPC": lambda: GethStartRPC(),
        "eth1/GethStopRPC": lambda: GethStopRPC(),
        "eth1/GethDatadir": lambda: GethDatadir(),
        # Parity
        "eth1/ParityGasCeiling": lambda arg=gasceiling: ParityGasCeiling(arg),
        "eth1/ParityDevLogs": lambda: ParityDevLogs(),
        "eth1/ParityGasFloor": lambda arg=gasfloor: ParityGasFloor(arg),
        "eth1/ParityUpgrade": lambda: ParityUpgrade(),
        "eth1/ParityTxPoolStatistics": lambda: ParityTxPoolStatistics(),
        "eth1/ParityTxCeiling": lambda arg=gas_limit: ParityTxCeiling(arg),
        "eth1/ParityMinGasPrice": lambda arg=gas_price: ParityMinGasPrice(arg),
        "eth1/ParitySyncMode": lambda arg=mode: ParitySyncMode(arg),
        "eth1/ParityChangeCoinbase": lambda arg=author: ParityChangeCoinbase(arg),
        "eth1/ParityChangeTarget": lambda arg=target_chain: ParityChangeTarget(arg),
        "eth1/ParityChangeExtra": lambda arg=extra_data: ParityChangeExtra(arg),
        "eth1/ParityDropPeers": lambda: ParityDropPeers(),
    }

    # Contains plugin names added with the `add` command.
    addedPlugins = set()

    def __init__(self) -> None:
        # Set node_type.
        if "Geth" in w3.clientVersion:
            self.node_type = NodeType.GETH
        elif "Parity" in w3.clientVersion:  # TODO: This is untested!
            self.node_type = NodeType.PARITY
        else:
            # TODO: Is this enough? Maybe make module inaccesible?
            cprint("Unsupported node type", "red")

        # Break w3.node_uri in prefix, host and port as expected by teatime.
        url = urlparse(w3.node_uri)
        self.prefix = url.scheme + "://"
        self.host = url.netloc + url.path
        if url.port is None:
            self.port = 8545  # Default port
        else:
            self.port = url.port

        pass

    @command("execute")
    def execute(self) -> str:
        """
        Execute RPC scanner
        """
        if not self.addedPlugins:
            cprint("No plugins selected")
            return

        # Create a list containing the instantiated plugins.
        instantiatedPlugins = []
        for plugin in self.addedPlugins:
            instantiatedPlugins.append(self.pluginInstantiator[plugin]())

        # Run a new scanner
        report = Scanner(
            self.host, self.port, self.node_type, instantiatedPlugins, self.prefix
        ).run()

        cprint("Scanreport: {}".format(report.to_dict()))

    # TODO: Support plugin=[str] as well
    @command("add")
    @argument(
        "plugin", description="add plugin to RPC scanner", choices=pluginInstantiator
    )
    def add(self, plugin: str) -> None:
        """
        Add plugin to RPC scanner
        """
        if plugin in self.pluginInstantiator and plugin in SUPPORTED_BY[self.node_type]:
            self.addedPlugins.add(plugin)
        else:
            cprint("plugin not supported by client or not existing")

    @command("rm")
    @argument(
        "plugin",
        description="remove plugin from RPC scanner",
        choices=pluginInstantiator,
    )
    def rm(self, plugin: str) -> None:
        """
        Remove plugin from RPC scanner
        """
        self.addedPlugins.discard(plugin)
