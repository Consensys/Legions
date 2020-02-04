from nubia import command, argument
from termcolor import cprint

# Mythril scanner
from mythril.mythril import MythrilAnalyzer
from mythril.mythril import MythrilDisassembler

from legions.commands.commands import w3
from legions.network.ethjsonrpc import EthJsonRpc

@command(aliases=["scan"])
@argument("contract", description="Address of the contract", aliases=["a"])
@argument("modules", description="Modules to load for the scan")
@argument("tx_count", description="Transaction count")
@argument("timeout", description="Scan timeout")
def scan(contract: str, modules = ["ether_thief", "selfdestruct"], tx_count: int = 2, timeout:int = 2):
    """
    Scan the contract with Mythril.
    """

    cprint("Scanning contract={} on node={}".format(contract, w3.node_uri))

    eth_json_rpc = EthJsonRpc(url=w3.node_uri)

    disassembler = MythrilDisassembler(
        eth=eth_json_rpc, solc_version=None, enable_online_lookup=True
    )
    disassembler.load_from_address(contract)

    analyzer = MythrilAnalyzer(
        strategy="bfs",
        onchain_storage_access=self.onchain_storage,
        disassembler=disassembler,
        address=contract,
        execution_timeout=timeout,
        loop_bound=3,
        max_depth=64,
        create_timeout=10,
    )

    report = analyzer.fire_lasers(
        modules=modules, transaction_count=tx_count
    )

    if len(report.issues) > 0:
        cprint(report.as_text())
    else:
        cprint("No issues found")