import requests
import json
from exception import ServerError

ENDPOINT = "https://testnet.accumulatenetwork.io/v1"
URL = "acc://d4c8d9ab07daeecf50a7c78ff03c6524d941299e5601e578/ACME"

JSONRPC_VERSION = "2.0"


class Accumulate():
    def __init__(self, endpoint: str) -> None:
        """
        API calls are made to a node endpoint, which is a URL. The base URL follows this format:
        [node-ip] is the IP address for the node you are connecting to.
        [http-port] is the port that the node you are connecting to is listening for HTTP calls.
        All API calls are made to the /v1 endpoint.

        Args:
            endpoint: the node endpoint URL
        """
        self.endpoint = endpoint
        self.id = 0

    def __generate_payload__(
        self, id, method: str, params: dict(), jsonrpc_version: str = JSONRPC_VERSION
    ):
        payload = {
            "jsonrpc": JSONRPC_VERSION,
            "id": id,
            "method": method,
            "params": params,
        }
        return payload

    def __id__(self):
        self.id += 1
        return self.id

    def get(self, url: str):
        """
        Returns Accumulate Object by URL

        Args:
            url: Any Accumulate URL

        Returns:
            type: The Accumulate object type
            mdRoot: The root hash (merkle DAG root) of the patricia trie
            data: The data for this object (properties vary)
            sponsor: The data for this object (properties vary)
            keyPage: The within key book for this ADI

        """
        params = {"url": url}
        method = "get"
        payload = self.__generate_payload__(self.__id__(), method, params)
        headers = {"content-type": "application/json"}
        res = requests.post(
            url=self.endpoint, headers=headers, data=json.dumps(payload)
        )
        res_text = json.loads(res.text)
        error_obj = res_text.get("error")
        if error_obj:
            error_obj.update({"id": res_text.get("id")})
            raise ServerError(error_obj)
        return res_text.get("result")


class Adi:
    def adi(self, url: str):
        """
        Returns information about the specified ADI

        Args:
            url: The ADI URL to check

        Returns:
            url: The URL for this ADI
            publicKeyHash: The SHA-256 hash of the Public Key for this ADI

        Raises:
            KeyError: Raises an exception.
        """
        pass


class Token:
    def token(self, url: str):
        """
        Returns Accumulate Object by URL

        Args:
            url: Any Accumulate URL

        Returns:
            This is a description of what is returned.

        Raises:
            KeyError: Raises an exception.
        """
        pass

    def token_account(self, url: str):
        """
        Returns Accumulate Object by URL

        Args:
            url: Any Accumulate URL

        Returns:
            This is a description of what is returned.

        Raises:
            KeyError: Raises an exception.
        """
        pass

    def token_account_history(self, url: str):
        """
        Returns Accumulate Object by URL

        Args:
            url: Any Accumulate URL

        Returns:
            This is a description of what is returned.

        Raises:
            KeyError: Raises an exception.
        """
        pass

    def token_tx(self, hash: str):
        """
        Returns Accumulate Object by URL

        Args:
            url: Any Accumulate URL

        Returns:
            This is a description of what is returned.

        Raises:
            KeyError: Raises an exception.
        """
        pass

    def faucet(self, url: str):
        """
        Returns Accumulate Object by URL

        Args:
            url: Any Accumulate URL

        Returns:
            This is a description of what is returned.

        Raises:
            KeyError: Raises an exception.
        """
        pass


class Key:
    def keypage(self, url: str):
        """
        Returns Accumulate Object by URL

        Args:
            url: Any Accumulate URL

        Returns:
            This is a description of what is returned.

        Raises:
            KeyError: Raises an exception.
        """
        pass

    def keybook(self, url: str):
        """
        Returns Accumulate Object by URL

        Args:
            url: Any Accumulate URL

        Returns:
            This is a description of what is returned.

        Raises:
            KeyError: Raises an exception.
        """
        pass


# a = Accumulate(ENDPOINT)
# try:
#     res = a.get(URL)
#     print(res)
# except Exception as e:
#     print(str(e))
