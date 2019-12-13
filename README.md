[<img width="200" alt="get in touch with Consensys Diligence" src="https://user-images.githubusercontent.com/2865694/56826101-91dcf380-685b-11e9-937c-af49c2510aa0.png">](https://diligence.consensys.net)<br/>
<sup>
[[  🌐  ](https://diligence.consensys.net)  [  📩  ](mailto:diligence@consensys.net)]
</sup><br/><br/>


# Legions
Ethereum Node Security Toolkit

Handy toolkit for (security) researchers poking around Ethereum nodes and contracts, now with a slick command-line interface, with auto complete commands and history.

Other functionalities:
 - Conversions (toWei, fromWei, keccak, etc)
 - Query for balance, code, storage of smart contracts, ecrecover
 - etc

**This package is extremely beta**

## Installation

Require `Python 3.7.0`.

```bash
clone https://github.com/shayanb/Legions
cd Legions
pip install .
```

or

```bash
pip install legions
```


## Usage

If installed locally:
```bash
python legions/main.py
```

or if installed globally:

```bash
legions
```

### Functions

![demo](https://github.com/shayanb/Legions/raw/master/assets/demo.gif "Demo")


| Command     | [Subcommand] |  Description                                                 |
|:-----------:|:------------|:--------------------------------------------------------------|
| **sethost** | | **Setup the Web3 connection (RPC, IPC, HTTP)** (default to infura mainnet)|
| **getnodeinfo**| | **Information about the connected node** (run `setnode` before this)   |
| **conversions** | | **Conversions possible to do with Web3**                              |
|            | fromWei    |  Converts the input to ether (to `currency` default to ether)   |
|            | toWei    |    Converts the input to Wei (from `currency` default to ether)   |
|            | keccak    |        keccak hash of the input                                  |
|            | toBytes    |      Converts the input to hex representation of its Bytes      |
|            | toChecksumAddress  |        Converts the input to Checksum Address           |
|            | toHex    |        Converts the input text to Hex                             |
|            | fromWei    |        Converts the input to ether (or specified currency)      |
| **query**      |     | **Query Blockchain (Storage, balance, etc)**                       |
|            | balance    |  Get Balance of an account                                      |
|            | block    |  Get block details by block number                                |
|            | code    |  Get code of the smart contract at address                         |
|            | ecrecover |  Get address associated with the signature (ecrecover)  `BUGGY`  |
|            | storage    |  Read the storage of a contract (`count` default = 10)          |
|            | command    |  Manual RPC method with args                                    |
| **investigate** | | **Investigate further in the node** (e.g. check if accounts are unlocked, etc) |
|            | accounts | Investigate accounts (e.g. check if accounts are unlocked, etc)   |
|            | admin| Investigate accounts (e.g. functionalities under the admin_ namespace)|
|            | sign    |  Investigate signature functionalities                             |       
| **version** | | **Print Versions** (If connected to a node it will print the host version too) |




## Acknowledgement
 - Interactive shell: [python-nubia](https://github.com/facebookincubator/python-nubia)
 - [Web3.py](https://github.com/ethereum/web3.py/)



## TODO:
 - Fix `Verbose` Status bar (It does not change from `OFF`)
 - Print Accounts in `getnodeinfo` in a pretty format (One per line)
 - A way to reinitiate w3 (web3) by setting it to new host (right now it works for sethost but getnodeinfo still uses the first initiated w3)
 - add way more functionalities
 - `chains.json` depending on the execution path might not be found. fix it.
 - inline TODOs (tons)


