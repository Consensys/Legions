from ens import ENS as _ens
from web3 import Web3
from termcolor import cprint
from nubia import command, argument
from legions.commands.commands import w3
import requests
import json
from tabulate import tabulate
from datetime import datetime

headers = {
    'authority': 'api.thegraph.com',
    'accept': '*/*',
    'content-type': 'application/json',
    'origin': 'https://app.ens.domains',
    'sec-fetch-site': 'cross-site',
    'dnt': '1',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'mode': 'cors',
    'credentials': 'omit'
}


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
        # cprint("Valid name: {}".format(self.ns.is_valid_name(name))) #is_valid_name returns true for any string? 

        if self.ns.is_valid_name(name):
            cprint("Namehash: {}".format(self.ns.namehash(name).hex()))
            if self.ns.owner(name) == "0x0000000000000000000000000000000000000000":
                cprint("Not Registered")
                return None
            cprint("Owner: {}".format(self.ns.owner(name)))
            # cprint("First Owner: {}".format(self.ns._first_owner((name))[0]))
            resolver = self.ns.resolver(name)
            if resolver is not None:
                cprint("Resolver: {}".format(resolver.address))
            else:
                cprint("No resolver is set")



    @command("listNames")
    @argument("address", description="list all ENS names owned by an address")
    def list(self, address: str) -> str:
        """
        List all ENS names owned by an address
        """

        cprint("Domains for '{}'".format(address))

        data = {"operationName" :"getRegistrations",
        "variables":{
            "id":"{}".format(address),
            "orderBy":"expiryDate",
            "orderDirection":"asc"
            }, #TODO: clear the graph Query to only the variables needed. Copied from ens.manager atm
        "query": "query getRegistrations($id: ID!, \
        $first: Int, $skip: Int, $orderBy: Registration_orderBy, \
            $orderDirection: OrderDirection) \
                {  account(id: $id)        \
                    {   registrations(     \
                        first: $first,     \
                        skip: $skip,       \
                        orderBy: $orderBy, \
                        orderDirection: $orderDirection) \
                        {                   \
                            expiryDate      \
                            domain {        \
                            labelName       \
                            labelhash       \
                            name            \
                            isMigrated      \
                            parent          \
                            {               \
                            name            \
                            __typename      \
                            }               \
                        __typename          \
                        }                   \
                    __typename              \
                    }                       \
                __typename  }}"
        }

        try:
            response = requests.post('https://api.thegraph.com/subgraphs/name/ensdomains/ens', json=data)

            if (response.status_code != 200):
                cprint("Query failed with {} error message: {} ".format(response.status_code, response.content), "red")
                return None

            names = []
            tableHeaders = ["Name", "Hash", "Expiry Date", "Migrated?"]
            for domainName in response.json().get("data", {}).get("account", {}).get("registrations", {}):
                names.append([domainName.get("domain", []).get("name", ""), 
                            domainName.get("domain", []).get("labelhash", ""), 
                            datetime.fromtimestamp(int(domainName.get("expiryDate", ""))), 
                            str(domainName.get("domain", []).get("isMigrated", ""))
                            ])
            cprint(tabulate(names, headers=tableHeaders, tablefmt = "pretty", stralign= "center"))

        except Exception as e:
            cprint("Failed to query: {}".format(response.content), "red")
            return 0

