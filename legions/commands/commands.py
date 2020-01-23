#!/usr/bin/env python3

# Legion - Shayan Eskandari, ConsenSys Diligence

import asyncio
import os
import socket
import typing
from termcolor import cprint
from nubia import command, argument
from legions.context import context
from web3 import Web3
import requests
from legions.commands.helper_functions import getChainName

w3 = Web3()
LEGION_VERSION = "0.5.2"
INFURA_URL = "https://mainnet.infura.io/v3/c3914c0859de473b9edcd6f723b4ea69"
PEER_SAMPLE = "enode://000331f91e4343a7145be69f1d455b470d9ba90bdb6d74fe671b28af481361c931b632f03c03dde5ec4c34f2289064ccd4775f758fb95e9496a1bd5a619ae0fe@lfbn-lyo-1-210-35.w86-202.abo.wanadoo.fr:30303"
# TODO ^ a real verbose node for this!


LEGION_TEST_PASS = (
    "Legion2019"  # TODO: there should be a better (recovarable) way to do this.
)
LEGION_TEST_PRV = "0x28d96497361cfc7cde5f253232d1ea300333891792d5922991d98683e1fb05c6"  # 0x9541ba003233f53afc11be1834f1fd26fb7c2060

Protocols = ["http", "rpc", "ipc", "ws"]
host = None


@command(aliases=["sethost"])
@argument("host", description="Address of the RPC Node", aliases=["u"])
def sethost(host: str):
    """
    Setup the Web3 connection (RPC, IPC, HTTP) - This should be the first step 
    """
    if host is None:
        cprint("Missing Argument 'host'?", "red")
        return 0

    ctx = context.get_context()
    cprint("Input: {}".format(host), "yellow")
    cprint("Verbose? {}".format(ctx.verbose), "yellow")

    w3 = Web3()
    if not any(ext in host for ext in Protocols):
        host = "https://" + host

    WEB3_PROVIDER_URI = host
    os.environ["WEB3_PROVIDER_URI"] = host

    if w3.isConnected():
        cprint("Web3 API Version: {}".format(w3.api), "green")
        cprint(
            "connected to: {}".format(w3.provider._active_provider.endpoint_uri),
            "green",
        )
        cprint("Version: {}".format(w3.clientVersion), "green")
    else:
        cprint("Web3 API Version: {}".format(w3.api), "red")
        cprint("Cannot connect to: {} ".format(host), "red")

    return 0


@command("getnodeinfo")
def getnodeinfo():
    """
    Prints information about the node (run setnode before this) 
    """
    if w3.isConnected():
        cprint("Web3 API Version: {}".format(w3.api), "white")
        cprint(
            "connected to: {}".format(w3.provider._active_provider.endpoint_uri),
            "white",
        )
        cprint("Version: {}".format(w3.clientVersion), "green")
        cprint("--" * 32)
        cprint("Last Block Number: {}".format(w3.eth.blockNumber), "green")
        cprint(
            "Chain: {} (ChainID: {})".format(
                getChainName(w3.eth.chainId), w3.eth.chainId
            ),
            "green",
        )
        cprint("Protocol Version: {}".format(w3.eth.protocolVersion), "green")
        cprint("Is Listening: {}".format(w3.net.listening), "green")
        cprint("Peer Count: {}".format(w3.net.peerCount), "green")
        cprint("Is Syncing: {}".format(w3.eth.syncing), "green")
        cprint("Is Mining: {}".format(w3.eth.mining), "green")
        cprint("Hash Rate: {}".format(w3.eth.hashrate), "green")
        cprint("Gas Price: {}".format(w3.eth.gasPrice), "green")
        cprint("--" * 32)
        try:
            cprint("Coinbase Account: {}".format(w3.eth.coinbase), "green")
        except Exception as e:
            cprint("Coinbase not available: {}".format(e), "red")
        cprint("Accounts", "green")
        for account in w3.eth.accounts:
            cprint("- {}".format(account), "green")
    else:
        cprint("Web3 API Version: {}".format(w3.api), "red")
        cprint("Cannot connect to: {} ".format(host), "red")
        cprint("Did you run sethost?", "red")
    return 0


@command("version")
def version():
    """
    Print Versions (If connected to a node it will print the host version too)
    """
    cprint("Legion Version: {}".format(LEGION_VERSION), "white")
    cprint("Web3 API Version: {}".format(w3.api), "white")
    if w3.isConnected():
        cprint(
            "connected to: {}".format(w3.provider._active_provider.endpoint_uri),
            "green",
        )
        cprint("Version: {}".format(w3.clientVersion), "green")
    else:
        cprint("Not connected to any hosts.", "red")


@command
class Investigate:
    "Investigate further in the node (e.g. check if accounts are unlocked, etc)"

    def __init__(self) -> None:
        if not (w3.isConnected()):
            cprint("Web3 API Version: {}".format(w3.api), "red")
            cprint("Cannot connect to: {} ".format(host), "red")
            cprint("Did you run sethost?", "red")
            return None

    """Investigate further in the node (e.g. check if accounts are unlocked, etc"""

    @command("accounts")
    @argument("all", description="Show me all the details", aliases=["A"])
    @argument(
        "intrusive",
        description="Be intrusive, try to make new accounts, etc",
        aliases=["i"],
    )
    def investigate_accounts(
        self, all: bool = True, intrusive: bool = True
    ):  # TODO: make these default to False for public use
        """
        Investigate accounts (e.g. check if accounts are unlocked, etc)
        """
        if w3.isConnected():
            coinbase = None
            try:
                coinbase = w3.eth.coinbase
            except Exception as e:
                cprint("Coinbase not available: {}".format(e), "red")
            accounts = w3.eth.accounts
            if len(accounts) == 0:
                cprint("No accounts found", "red")
                if (
                    type(coinbase) is None
                ):  # TODO: check if we need this. If accounts = [] , then there shouldn't be coinbase (?)
                    cprint("Nothing to do here")
                    return 0

            if all:
                for account in accounts:
                    cprint(
                        "Balance of {} is : {}".format(
                            account, w3.eth.getBalance(account)
                        ),
                        "white",
                    )
                    # try:
                    #     cprint("Trying to unlock {}: {}".format(account, w3.parity.personal.unlockAccount(account, "")), "white")
                    # except Exception as e:
                    #     cprint("Failed to unlock: {}".format(e))
                    pass
            else:
                cprint("Number of Accounts: {}".format(len(w3.eth.accounts)), "green")

            # cprint("logs: {}".format(w3.eth.getLogs()), "white") #needs to pass filter_params --> maybe based on the accounts? filter events of the accounts hu?

            if "parity" in (w3.clientVersion.lower()):
                ww3 = w3.parity
            elif "geth" in (w3.clientVersion.lower()):
                ww3 = w3.geth

            if intrusive:
                try:
                    cprint(
                        "importRawKey: {}".format(
                            ww3.personal.importRawKey(LEGION_TEST_PRV, LEGION_TEST_PASS)
                        ),
                        "green",
                    )
                except Exception as e:
                    cprint("importRawKey: {}".format(e), "yellow")
                try:
                    cprint(
                        "newAccount: {}".format(
                            ww3.personal.newAccount(LEGION_TEST_PASS)
                        ),
                        "white",
                    )
                except Exception as e:
                    cprint("newAccount: {}".format(e), "yellow")

            cprint("--" * 32)

    @command("admin")
    @argument(
        "intrusive", description="Be intrusive, try to add peers, etc", aliases=["i"]
    )
    def investigate_admin(
        self, intrusive: bool = False
    ):  # TODO: make these default to False for public use
        """
        Investigate accounts (e.g. functionalities under the admin_ namespace)
        """
        cprint("clientVersion: {}".format(w3.clientVersion), "white")
        # More interfaces here: https://web3py.readthedocs.io/en/stable/web3.geth.html
        if "geth" in (
            w3.clientVersion.lower()
        ):  # TODO: make this figure out if the node is Geth or Parity and send the appropriate commands
            if intrusive:
                try:
                    cprint(
                        "AddPeer: {}".format(w3.geth.admin.add_peer(PEER_SAMPLE)),
                        "green",
                    )
                except Exception as e:
                    cprint("AddPeer: {}".format(e), "yellow")

            try:
                cprint("datadir: {}".format(w3.geth.admin.datadir()), "green")
            except Exception as e:
                cprint("datadir: {}".format(e), "yellow")
            try:
                cprint("nodeInfo: {}".format(w3.geth.admin.nodeInfo()), "green")
            except Exception as e:
                cprint("nodeInfo {}".format(e), "yellow")
            try:
                cprint("peers: {}".format(w3.geth.admin.peers()), "green")
            except Exception as e:
                cprint("peers {}".format(e), "yellow")
            try:
                cprint("txpool.status: {}".format(w3.geth.txpool.status()), "green")
            except Exception as e:
                cprint("txpool.status {}".format(e), "yellow")
            try:
                cprint("shh.version: {}".format(w3.geth.shh.version()), "green")
            except Exception as e:
                cprint("shh.version: {}".format(e), "yellow")
            try:
                cprint("Wshh.info: {}".format(w3.geth.shh.info()), "green")
            except Exception as e:
                cprint("shh.info: {}".format(e), "yellow")

        elif "parity" in (w3.clientVersion.lower()):
            try:
                cprint("versionInfo: {}".format(w3.parity_versionInfo()), "green")
            except Exception as e:
                cprint("versionInfo: {}".format(e), "yellow")
        #     try:
        #         cprint("nodeInfo: {}".format(w3.parity_lockedHardwareAccountsInfo()), "green")
        #     except Exception as e:
        #         cprint("nodeInfo {}".format(e), "yellow")
        #     try:
        #         cprint("peers: {}".format(w3.parity_localTransactions()), "green")
        #     except Exception as e:
        #         cprint("peers {}".format(e), "yellow")
        #     try:
        #         cprint("txpool.status: {}".format(w3.make_request("parity_listVaults", [])), "green")
        #     except Exception as e:
        #         cprint("txpool.status {}".format(e), "yellow")
        #     try:
        #         cprint("shh.version: {}".format(w3.parity.shh.__dict__), "green")
        #     except Exception as e:
        #         cprint("shh.version: {}".format(e), "yellow")
        #     try:
        #         cprint("Wshh.info: {}".format(w3.parity.shh.info()), "green")
        #     except Exception as e:
        #         cprint("shh.info: {}".format(e), "yellow")

    @command("sign")
    # @argument("all", description="Show me all the details", aliases=["A"])
    # @argument("intrusive", description="Be intrusive, try to make new accounts, etc", aliases=["i"])
    def investigate_sign(
        self, msg: str = "Legions Test", account: str = None, intrusive: bool = True
    ):
        """
        Investigate signature functionalities 
        """
        if w3.isConnected():
            coinbase = None
            try:
                coinbase = w3.eth.coinbase
            except Exception as e:
                cprint("Coinbase not available: {}".format(e), "red")
            accounts = w3.eth.accounts
            if len(accounts) == 0:
                cprint("No accounts found", "red")
                if (
                    type(coinbase) is None
                ):  # TODO: check if we need this. If accounts = [] , then there shouldn't be coinbase (?)
                    cprint("Nothing to do here")
                    return 0

            if account is None:
                for account in accounts:
                    try:
                        cprint(
                            "Signing {} by {} : {}".format(
                                msg, account, w3.eth.sign(account, text=msg)
                            ),
                            "white",
                        )
                    except Exception as e:
                        cprint("failed to sign by {}: ".format(account, e))
            else:
                try:
                    cprint(
                        "Signing {} by {} : {}".format(
                            msg, account, w3.eth.sign(account, text=msg)
                        ),
                        "white",
                    )
                except Exception as e:
                    cprint("failed to sign by {}: ".format(account, e))

            # TODO:
            # Implement for other types and not just text: Eth.sign(account, data=None, hexstr=None, text=None)
            # Also for : Eth.signTypedData


@command
class Query:
    "Query Blockchain (Storage, balance, etc)"

    def __init__(self) -> None:
        if not (w3.isConnected()):
            cprint("Web3 API Version: {}".format(w3.api), "white")
            cprint(
                "Not using a custom node. Run sethost to connect to your node", "red"
            )
            os.environ[
                "WEB3_PROVIDER_URI"
            ] = INFURA_URL  # TODO: Better default web3 instance?
            cprint("Connecting to Infura...", "green")

    @command("balance")
    @argument("address", description="Address of the account", aliases=["a"])
    @argument(
        "block",
        description="(Optional) Block number for the query (default latest)",
        aliases=["b"],
    )
    def get_balance(self, address: str, block: int = None):  #  -> int:
        """
        Get Balance of an account
        """

        if address is None:
            cprint("Missing Argument 'address'?", "red")
            return 0

        if block is None:
            block = w3.eth.blockNumber

        address = Web3.toChecksumAddress(address)
        balance = w3.eth.getBalance(address, block_identifier=block)
        cprint(
            "Balance of {} is : {} wei ({} Eth)".format(
                address, balance, Web3.fromWei(balance, "ether")
            ),
            "green",
        )

    @command("storage")
    @argument("address", description="Address of the account", aliases=["a"])
    @argument("count", description="Number of storage slots to read", aliases=["i"])
    @argument(
        "block",
        description="(Optional) Block number for the query (default latest)",
        aliases=["b"],
    )
    def get_storage(self, address: str, count: int = 10, block: int = None):
        """
        Get the first "count" number of an address. count default = 10
        """

        if address is None:
            cprint("Missing Argument 'address'?", "red")
            return 0

        if block is None:
            block = w3.eth.blockNumber

        address = Web3.toChecksumAddress(address)
        for i in range(0, count):
            hex_text = None
            # print(Web3.isAddress(Web3.toHex(w3.eth.getStorageAt(address, i))), Web3.toHex(w3.eth.getStorageAt(address, i))) #TODO: detect address

            try:  # TODO: make this smarter, detect the variable and show proper represantation of it .
                hex_text = Web3.toText(
                    w3.eth.getStorageAt(address, i, block_identifier=block)
                )
            except:
                try:
                    hex_text = Web3.toInt(
                        w3.eth.getStorageAt(address, i, block_identifier=block)
                    )
                except:
                    hex_text = None

            cprint(
                "Storage {} = {} ({})".format(
                    i,
                    Web3.toHex(w3.eth.getStorageAt(address, i, block_identifier=block)),
                    hex_text,
                ),
                "green",
            )

    @command("code")
    @argument("address", description="Address of the account", aliases=["a"])
    @argument(
        "block",
        description="(Optional) Block number for the query (default latest)",
        aliases=["b"],
    )
    def get_code(self, address: str, block: int = None):
        """
        Get code of the smart contract at address
        """

        if address is None:
            cprint("Missing Argument 'address'?", "red")
            return 0

        if block is None:
            block = w3.eth.blockNumber

        address = Web3.toChecksumAddress(address)
        cprint(
            "Code of {} = \n {}".format(
                address, Web3.toHex(w3.eth.getCode(address, block_identifier=block))
            ),
            "yellow",
        )

    @command("block")
    @argument("block", description="Block number (default latest)", aliases=["b"])
    def get_block(self, block: int = None):
        """
        Get block details by block number
        """

        if block is None:
            block = w3.eth.blockNumber

        cprint(
            "block {} details = \n {}".format(
                block, (w3.eth.getBlock(block_identifier=block))
            ),
            "yellow",
        )  # TODO: make this print pretty json

    @command("transaction")
    @argument("hash", description="Transaction hash to query", aliases=["t"])
    @argument(
        "block",
        description="(Optional) Block number for the query (default latest)",
        aliases=["b"],
    )
    def get_transaction(self, hash: str, block: int = None):
        """
        Get transaction details by hash
        """

        if hash is None:
            cprint("Missing Argument 'hash'?", "red")
            return 0

        if block is None:
            block = w3.eth.blockNumber

        cprint(
            "transaction {} details = \n {}".format(
                hash, (w3.eth.getTransaction(hash))
            ),
            "yellow",
        )  # TODO: make this print pretty json

    @command("command")
    @argument("method", description="RPC Method to be used (e.g. eth_getBalance)")
    @argument("args", description="Arguments for the RPC method (comma separated)")
    @argument(
        "block",
        description="(Optional) Block number for the query (default latest)",
        aliases=["b"],
    )
    def get_transaction(self, method: str, args: str = None, block: int = None):
        """
        Manual RPC method with args
        """

        if method is None:
            cprint("Missing Argument 'method'?", "red")
            return 0

        if block is None:
            block = w3.eth.blockNumber

        try:
            cprint(
                "{}({}): {} \n".format(
                    method,
                    args,
                    w3.manager.request_blocking(method, [str(args), block]),
                ),
                "green",
            )
        except Exception as e:
            cprint("failed {}({}) :  {} \n".format(method, args, e), "yellow")

    @command("ecrecover")
    @argument("data", description="The data which hash was signed")
    @argument("dataHash", description="The hash of the data")
    @argument("signedData", description="Signed data")
    def get_ecrecover(self, signedData: str, data: str = None, dataHash: str = None):
        """
        Get address associated with the signature (ecrecover)
        """
        if (data is None) and (dataHash is None):
            cprint(
                "Missing Argument, either 'dataHash' or 'data' must be passed?", "red"
            )
            return 0

        try:
            if data is not None:
                from eth_account.messages import encode_defunct, _hash_eip191_message

                hex_message_hash = w3.toHex(
                    _hash_eip191_message(encode_defunct(hexstr=data))
                )
            elif dataHash is not None:
                hex_message_hash = dataHash

            sig = w3.toBytes(hexstr=signedData)
            v, hex_r, hex_s = (
                w3.toInt(sig[-1]),
                w3.toHex(sig[:32]),
                w3.toHex(sig[32:64]),
            )
            address = w3.eth.account.recoverHash(hex_message_hash, signature=sig)
            # TODO: verify this! seems that sometimes it returns wrong address
            # test with :
            #           data="0xd46e8dd67c5d32be8d46e8dd67c5d32be8058bb8eb970870f072445675058bb8eb970870f072445675"
            #           signedData="0xe7225f986f192f859a9bf84e34b2b7001dfa11aeb5c7164f81a2bee0d79943e2587be1faa11502eba0f803bb0ee071a082b6fe40fba025f3309263a1eef52c711c"
            #       Correct address: 0xb60e8dd61c5d32be8058bb8eb970870f07233155  //based on https://wiki.parity.io/JSONRPC-personal-module.html#personal_ecrecover
            #       Returned address: 0x02F0D4b967a73D6907a221DB6106446F1d3d4CDB

            cprint(
                "Address: {}".format(address), "green"
            )  # TODO: make this print pretty json
            cprint("r: {}\ns: {}\nv: {} ".format(hex_r, hex_s, v), "white")
        except Exception as e:
            cprint("failed to get address: {} \n".format(e), "yellow")
