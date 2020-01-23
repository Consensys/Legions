import requests
import json
from termcolor import cprint


ChainID_JSON = "chains.json"


def checkConnection(url, verbose=None):
    r = requests.get(url, timeout=5)
    if verbose:
        cprint("Status Code: {}".format(r.status_code), "grey")
        cprint("Response: {}".format(r.text), "grey")
    if r.status_code not in [400, 404, 503]:
        return True
    else:
        return False


def getChainName(ChainID, json_file=ChainID_JSON):
    # chain list Source: https://chainid.network/
    # TODO: make this nicer
    try:
        with open(json_file, "r") as f:
            chains_dict = json.load(f)
        for chain in chains_dict:
            print
            if chain.get("chainId", None) == ChainID:
                return chain.get("name")
    except Exception as e:
        print("Failed to find the chainID for {} - {}".format(ChainID, e))
        return ""
