# Legions
Ethereum Node Security Toolkit

Handy toolkit for security researchers poking around Ethereum nodes (and contracts)

**This package is extremely beta**

## Installation

`Python 3.7.0`

```bash
clone https://github.com/shayanb/Legions
cd Legions
pip install .
```

or

```
pip install legions
```


## Usage

```
legions
```

| Command     | Description                                                                |
| ------------- |------------- |
| getnodeinfo | Prints information about the node (run setnode before this)                |
| investigate | Investigate further in the node (e.g. check if accounts are unlocked, etc) |
| query       | Query Blockchain (Storage, balance, etc)                                   |
| sethost     | Setup the Web3 connection (RPC, IPC, HTTP) - This should be the first step |
| version     | Print Versions (If connected to a node it will print the host version too) |


![demo](https://github.com/shayanb/Legions/raw/master/assets/demo.gif "Demo")



## Acknowledgement
 - Interactive shell: [python-nubia](https://github.com/facebookincubator/python-nubia)
 - [Web3.py](https://github.com/ethereum/web3.py/)



## TODO:
 - Fix `Verbose` Status bar (It does not change from `OFF`)
 - Print Accounts in `getnodeinfo` in a better format (One per line)
 - A way to reinitiate w3 (web3) by setting it to new host (right now it works for sethost but getnodeinfo still uses the first initiated w3)
 - add way more functionalities
 - `chains.json` depending on the execution path might not be found. fix it.
 - inline TODOs (tons)
 - 


