#!/usr/bin/env python3

# Legion - Shayan Eskandari, ConsenSys Diligence

import asyncio
import os
import socket
import typing
from termcolor import cprint
from nubia import command, argument
from legion_context import context
from web3 import Web3
import requests
from helper_functions import getChainName

w3 = Web3()
LEGION_VERSION = "0.0.1"

Protocols = ["http", "rpc", "ipc", "ws"]
url = ""

@command(aliases=["sethost"])
@argument("host", description="Address of the RPC Node", aliases=["u"])
def sethost(host: typing.List[str]):
    """
    Setup the Web3 connection (RPC, IPC, HTTP) - This should be the first step 
    """
    if (host is None):
        cprint("Missing Argument 'host'?", "red")
        return 0

    ctx = context.get_context()
    cprint("Input: {}".format(host), "yellow")
    cprint("Verbose? {}".format(ctx.verbose), "yellow")

    w3 = Web3()
    url = host[0]
    if not any(ext in url for ext in Protocols):
        url = "https://" + url

    # if helper_functions.checkConnection(url = url, verbose=True)
    WEB3_PROVIDER_URI = url
    os.environ["WEB3_PROVIDER_URI"] = url

    if (w3.isConnected()):
        cprint("Web3 API Version: {}".format(w3.api), "green")
        cprint("connected to: {}".format(w3.provider._active_provider.endpoint_uri), "green")
        cprint("Version: {}".format(w3.clientVersion), "green")
    else:
        cprint("Web3 API Version: {}".format(w3.api), "red")
        cprint("Cannot connect to: {} ".format(url), "red")

    # optional, by default it's 0
    return 0


@command("getnodeinfo")
def getnodeinfo():
    """
    Prints information about the node (run setnode before this) 
    """
    if (w3.isConnected()):
        cprint("Web3 API Version: {}".format(w3.api), "white")
        cprint("connected to: {}".format(w3.provider._active_provider.endpoint_uri), "white")
        cprint("Version: {}".format(w3.clientVersion), "green")
        cprint("--" * 32)
        cprint("Last Block Number: {}".format(w3.eth.blockNumber), "green")
        cprint("Chain: {}(ChainID: {})".format(getChainName(w3.eth.chainId), w3.eth.chainId), "green")
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
            
        cprint("Accounts: {}".format(w3.eth.accounts), "green")    
    else:
        cprint("Web3 API Version: {}".format(w3.api), "red")
        cprint("Cannot connect to: {} ".format(url), "red")
        cprint("Did you run sethost?", "red")

    # optional, by default it's 0
    return 0

@command("version")
def version():
    """
    Print Versions (If connected to a node it will print the host version too)
    """
    cprint("Legion Version: {}".format(LEGION_VERSION), "white")
    cprint("Web3 API Version: {}".format(w3.api), "white")
    if (w3.isConnected()):
        cprint("connected to: {}".format(w3.provider._active_provider.endpoint_uri), "green")
        cprint("Version: {}".format(w3.clientVersion), "green")
    else:
        cprint("Not connected to any hosts.", "red")


# @command
# @argument("number", type=int)
# async def triple(number):
#     "Calculates the triple of the input value"
#     cprint("Input is {}".format(number))
#     cprint("Type of input is {}".format(type(number)))
#     cprint("{} * 3 = {}".format(number, number * 3))
#     await asyncio.sleep(2)


# @command
# @argument("style", description="Pick a style", choices=["test", "toast", "toad"])
# @argument("stuff", description="more colors", choices=["red", "green", "blue"])
# @argument("code", description="Color code", choices=[12, 13, 14])
# def pick(style: str, stuff: typing.List[str], code: int):
#     """
#     A style picking tool
#     """
#     cprint("Style is '{}' code is {}".format(style, code), "yellow")


# instead of replacing _ we rely on camelcase to - super-command


# @command
# class SuperCommand:
#     "This is a super command"

#     def __init__(self, shared: int = 0) -> None:
#         self._shared = shared

#     @property
#     def shared(self) -> int:
#         return self._shared

#     """This is the super command help"""

#     @command
#     @argument("firstname", positional=True)
#     def print_name(self, firstname: str):
#         """
#         print a name
#         """
#         cprint("My name is: {}".format(firstname))

#     @command(aliases=["do"])
#     def do_stuff(self, stuff: int):
#         """
#         doing stuff
#         """
#         cprint("stuff={}, shared={}".format(stuff, self.shared))
