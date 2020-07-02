<img width="200" align="right" src="/assets/logo.png"></img>
<br>
[<img width="200" alt="get in touch with ConsenSys Diligence" src="https://user-images.githubusercontent.com/2865694/56826101-91dcf380-685b-11e9-937c-af49c2510aa0.png">](https://diligence.consensys.net)
<br/>
<sup>
[[  🌐  ](https://diligence.consensys.net)  [  📩  ](mailto:diligence@consensys.net)]
</sup><br/><br/>


# Legions
### EVM Node Security Toolkit

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![CircleCI](https://circleci.com/gh/ConsenSys/Legions/tree/master.svg?style=shield)](https://circleci.com/gh/ConsenSys/Legions/tree/master)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![PyPI](https://img.shields.io/pypi/v/legions.svg)](https://pypi.org/project/legions/)


Legions is a handy toolkit for (security) researchers poking around EVM (Ethereum Virtual Machine) nodes and smart contracts, now with a slick command-line interface, with auto complete commands and history.

### Features:
 - **Node detection** (`getnodeinfo`)
   - Detect the type of the Node, Chain, and Network
   - Peer Count, Listening, Synching, and Mining status
   - Gas Price
   - etc
 - **Web3 API enumeration** (`investigate`)
   - Accounts
     - Read coinbase, and accounts of the address
     - (`intrusive = True`) will try to create accounts on the node
   - Admin
     - Enumerates web3.admin endpoints
   - Sign (WIP)
     - Enumerates signing functionalities (web3.sign)
 - **ENS Queries** (`ens`)
   - List Names owned by an address
   - List Subdomains of an address
   - Query individual names
 - **Query** at latest/specific block number (`query`)
   - Balance of an address
   - Block details
   - Bytecode of the smart contract
   - Read storage of the smart contract (default `count=10` reads the first 10 slots)
   - command, which you can pass any RPC method with args
   - ECRecover of a signature
 - **Conversions** (toWei, fromWei, keccak, toChecksumAddress, etc)


**This tool is in beta and a work in progress**

### Demo

#### Main Functionality

![demo](/assets/main.gif "Main Functionality")

#### ENS (Ethereum Name Service)

![demo](/assets/ens.gif "Ethereum Name Service")



## Installation

Require `Python 3.6`.

```bash
pip install legions
```

Or directly from source code:

```bash
git clone https://github.com/shayanb/Legions
cd Legions
pip install .
```


## Usage

If installed locally:
```bash
python legions.py
```

or if installed globally:

```bash
legions
```

## Functions Breakdown 

|     Command     |   [Subcommand]    |                                  Description                                   |
| :-------------: | :---------------- | :----------------------------------------------------------------------------- |
|   **sethost**   |                   | **Setup the Web3 connection (RPC, IPC, HTTP)** (default to infura mainnet)     |
| **getnodeinfo** |                   | **Information about the connected node** (run `setnode` before this)           |
| **conversions** |                   | **Conversions possible to do with Web3**                                       |
|                 | fromWei           | Converts the input to ether (to `currency` default to ether)                   |
|                 | toWei             | Converts the input to Wei (from `currency` default to ether)                   |
|                 | keccak            | keccak hash of the input                                                       |
|                 | toBytes           | Converts the input to hex representation of its Bytes                          |
|                 | toChecksumAddress | Converts the input to Checksum Address                                         |
|                 | toHex             | Converts the input text to Hex                                                 |
|                 | fromWei           | Converts the input to ether (or specified currency)                            |
|    **query**    |                   | **Query Blockchain (Storage, balance, etc)**                                   |
|                 | balance           | Get Balance of an account                                                      |
|                 | block             | Get block details by block number                                              |
|                 | code              | Get code of the smart contract at address                                      |
|                 | ecrecover         | Get address associated with the signature (ecrecover)  `BUGGY`                 |
|                 | storage           | Read the storage of a contract (`count` default = 10)                          |
|                 | command           | Manual RPC method with args                                                    |
| **investigate** |                   | **Investigate further in the node** (e.g. check if accounts are unlocked, etc) |
|                 | accounts          | Investigate accounts (e.g. check if accounts are unlocked, etc)                |
|                 | admin             | Investigate accounts (e.g. functionalities under the admin_ namespace)         |
|                 | sign              | Investigate signature functionalities                                          |
|     **ens**     |                   | **Do Ethereum Name Service queries (supported on the mainnet only)**           |
|                 | toName            | Transform an address to the ENS name                                           |
|                 | toAddress         | Transform an ENS name to the Ethereum public address                           |
|                 | info              | Get details about an ENS name                                                  |
|   **version**   |                   | **Print Versions** (If connected to a node it will print the host version too) |




## Acknowledgements
 - Interactive shell: [python-nubia](https://github.com/facebookincubator/python-nubia)
 - [Web3.py](https://github.com/ethereum/web3.py/)
 - Node data provided by [chainid.network](https://chainid.network/)
 - ENS data provided by ENS GraphQL dataset



## TODO:
  - [ ] eth 2.0 API implementation
  - [ ] Fix `Verbose` Status bar (It does not change from `OFF`)
  - [ ] inline TODOs (tons)
  - [ ] resolve mappings from storage (using ABI?)
  - [ ] Get tokens Balance (etherscan or other explorer API)



