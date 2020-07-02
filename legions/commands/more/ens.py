from ens import ENS as _ens
from web3 import Web3
from termcolor import cprint
from nubia import command, argument
from legions.commands.commands import w3
import requests
import json
from tabulate import tabulate
from datetime import datetime


@command
class ens:
    "Ethereum Name Service Tools"

    def __init__(self) -> None:
        self.ns = _ens.fromWeb3(w3)
        pass

    @command("toName")
    @argument("address", description="reverse lookup name resolved from an address")
    def toName(self, address: str) -> str:
        """
        Reverse Lookup name resolved from an address
        """

        try:
            cprint("Name of {}: {}".format(address, self.ns.name(address)))
        except Exception as e:
            cprint("Failed to convert {}: {}".format(address, e), "yellow")

    @command("toAddress")
    @argument("name", description="lookup the address resolving by an ENS name")
    def toAddress(self, name: str) -> str:
        """
        Lookup the address resolving by an ENS name
        """

        try:
            cprint("Address of {}: {}".format(name, self.ns.address(name)))
        except Exception as e:
            cprint("Failed to lookup {}: {}".format(name, e), "yellow")

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
    @argument(
        "labelHash", description="Show full labelHash if name does not resolve",
    )
    def listNames(self, address: str, labelHash: bool = False) -> str:
        """
        List all ENS names owned by an address
        """

        cprint("## Names for '{}'".format(address))

        data = {
            "operationName": "getRegistrations",
            "variables": {
                "id": "{}".format(address.lower()),
                "orderBy": "expiryDate",
                "orderDirection": "asc",
            },  # TODO: clear the graph Query to only the variables needed. Copied from ens.manager atm
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
                            registrationDate \
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
                __typename  }}",
        }

        try:
            response = requests.post(
                "https://api.thegraph.com/subgraphs/name/ensdomains/ens", json=data
            )
            if response.status_code != 200:
                cprint(
                    "Query failed with {} error message: {} ".format(
                        response.status_code, response.content
                    ),
                    "red",
                )
                return None

            names = []
            tableHeaders = [
                "Name",
                "Hash",
                "Registration Date",
                "Expiry Date",
                "Migrated?",
            ]
            for domainName in (
                response.json()
                .get("data", {})
                .get("account", {})
                .get("registrations", {})
            ):
                names.append(
                    [
                        domainName.get("domain", {}).get("name", "")
                        if labelHash
                        else domainName.get("domain", []).get("labelName", ""),
                        domainName.get("domain", {}).get("labelhash", ""),
                        datetime.fromtimestamp(
                            int(domainName.get("registrationDate", ""))
                        ),
                        datetime.fromtimestamp(int(domainName.get("expiryDate", ""))),
                        str(domainName.get("domain", {}).get("isMigrated", "")),
                    ]
                )
            cprint(
                tabulate(
                    names, headers=tableHeaders, tablefmt="pretty", stralign="center"
                )
            )

        except Exception as e:
            cprint("Failed to query: {}".format(e), "red")
            return 0

    @command("listSubdomains")
    @argument("name", description="list all ENS sub domains of a name")
    @argument(
        "labelHash", description="Show full labelHash if name does not resolve",
    )
    def listSubdomains(self, name: str, labelHash: bool = False) -> str:
        """
        List all ENS sub domains of a name
        """

        cprint("## Subdomains for '{}'".format(name))

        nameHash = self.ns.namehash(name).hex()
        cprint("NameHash: '{}'".format(nameHash))

        data = {
            "operationName": "getSubdomains",
            "variables": {
                "id": "{}".format(nameHash)
            },  # TODO: clear the graph Query to only the variables needed. Copied from ens.manager atm
            "query": "query getSubdomains($id: ID!) \
                {  domain(id: $id)          \
                    {                       \
                    id                      \
                    labelName               \
                    subdomains              \
                        {                   \
                            id              \
                            labelName       \
                            labelhash       \
                            isMigrated      \
                            name            \
                            owner           \
                            {               \
                            id              \
                            __typename      \
                            }               \
                        __typename          \
                        }                   \
                __typename                  \
                }}",
        }

        try:
            response = requests.post(
                "https://api.thegraph.com/subgraphs/name/ensdomains/ens", json=data
            )
            if response.status_code != 200:
                cprint(
                    "Query failed with {} error message: {} ".format(
                        response.status_code, response.content
                    ),
                    "red",
                )
                return None

            names = []
            tableHeaders = ["Subdomain", "Owner", "Label Hash", "Migrated?"]
            for subDomain in (
                response.json().get("data", {}).get("domain", {}).get("subdomains", {})
            ):
                names.append(
                    [
                        subDomain.get("name", "")
                        if labelHash
                        else subDomain.get("labelName", ""),
                        subDomain.get("owner", {}).get("id", ""),
                        subDomain.get("labelhash", ""),
                        str(subDomain.get("isMigrated", "")),
                    ]
                )
            cprint(
                tabulate(
                    names, headers=tableHeaders, tablefmt="pretty", stralign="center"
                )
            )

        except Exception as e:
            cprint("Failed to query: {}".format(e), "red")
            return 0
