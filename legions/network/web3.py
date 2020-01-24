import os

from web3 import Web3 as _web3
from web3 import IPCProvider, HTTPProvider, WebsocketProvider


class Web3(_web3):
    """
    Web3 class
    """

    def __init__(self) -> None:
        self.node_uri = None

        super().__init__(HTTPProvider("null"))

    def connect(self, node: str, timeout: int = 10) -> None:
        self.node_uri = node

        try:
            if os.path.exists(node):
                self.provider = IPCProvider(node)
                return
        except OSError:
            pass

        if node.startswith("https://") or node.startswith("http://"):
            self.provider = HTTPProvider(node, request_kwargs={"timeout": timeout})
        elif node.startswith("ws://"):
            self.provider = WebsocketProvider(
                node, websocket_kwargs={"timeout": timeout}
            )
        else:
            raise ValueError(
                "The provided node is not valid. It must start with 'http://' or 'https://' or 'ws://' or a path to an IPC socket file."
            )
