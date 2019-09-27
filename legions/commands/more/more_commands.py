#!/usr/bin/env python3

# Legion - Shayan Eskandari, ConsenSys Diligence

from nubia import command, argument
from web3 import Web3
w3 = Web3()
from termcolor import cprint


@command
class Conversions:
    "Conversions possible to do with Web3"

    def __init__(self) -> None:
        pass

    """Conversions possible to do with Web3 (e.g. toWei, toHex, toChecksumAddress, keccak, etc"""

    @command("toHex")
    @argument("value", description="value to be converted")
    def toHex(self, value:str) -> str:
        """
        Converts the input text to Hex
        """
        try:
            cprint("Hex of {}: {}".format(value, w3.toHex(text=value)), "green")
        except Exception as e:
            cprint("Failed to convert {}: {} ".format(value, e), "yellow")


    @command("toText")
    @argument("value", description="value to be converted")
    def toText(self, value:str) -> str:
        """
        Converts the input Hex to Text
        """
        try:
            cprint("Text of {}: {}".format(value, w3.toText(value)), "green")
        except Exception as e:
            cprint("Failed to convert {}: {} ".format(value, e), "yellow")

    @command("toBytes") #Does not really make sense to have this, but meh.
    @argument("value", description="value to be converted")    
    def toBytes(self, value:str) -> str:
        """
        Converts the input to Bytes
        """
        try:
            cprint("Bytes of {}: {}".format(value, w3.toBytes(text=value)), "green")
        except Exception as e:
            cprint("Failed to convert {}: {} ".format(value, e), "yellow")


    @command("toWei")
    @argument("value", description="value to be converted")
    @argument("currency", description="type of the input, unit of currency")
    def toWei(self, value:float, currency:str = "ether") -> str:
        """
        Converts the input to Wei 
        """
        try:
            cprint("toWei {}: {}".format(value, w3.toWei(value, currency)), "green")
        except Exception as e:
            cprint("Failed to convert {} to {}: {}".format(value, currency, e), "yellow")


    @command("fromWei")
    @argument("value", description="value to be converted")
    @argument("currency", description="type of the output, unit of currency")
    def fromWei(self, value:int, currency:str = "ether") -> str:
        """
        Converts the input to ether (or specified currency)
        """
        try:
            cprint("fromWei {} to {}: {:18f}".format(value, currency, w3.fromWei(value, currency)), "green")
        except Exception as e:
            cprint("Failed to convert {} to {}: {}".format(value,currency, e), "yellow")

    @command("toChecksumAddress")
    @argument("value", description="value to be converted")
    def toChecksumAddress(self, value:str) -> str:
        """
        Converts the input to Checksum Address
        """
        try:
           cprint("toChecksumAddress of {}: {}".format(value, w3.toChecksumAddress(value)), "green")
        except Exception as e:
            cprint("Failed to toChecksumAddress {}: {}".format(value, e), "yellow")

    @command("keccak")
    @argument("value", description="value to be hashed")
    def keccak(self, value:str) -> str:
        """
        keccak hash of the input
        """
        #TODO: support hex_str too
        try:
            cprint("keccak of {}: {}".format(value, w3.toHex(w3.keccak(text=value))), "green")
        except Exception as e:
            cprint("Failed to get keccak of {}: {}".format(value, e), "yellow")


    # @command("solidityKeccak")
    # @argument("value", description="value to be hashed")
    # @argument("type", description="Solidity type of the value")
    # def solidityKeccak(self, value:str, type:str) -> str:
    #     """
    #     solidityKeccak hash of the input
    #     """
    #     #TODO: fix this: Failed to get solidityKeccak of test: Could not discover provider while making request: method:net_version
    #     #TODO: better type identification
    #     #TODO: accept lists as input
    #     try:
    #         cprint("solidityKeccak of {}:{}: {}".format(value,type, w3.toHex(w3.solidityKeccak([type], [value]))), "green")
    #     except Exception as e:
    #         cprint("Failed to get solidityKeccak of {}: {}".format(value, e), "yellow")
