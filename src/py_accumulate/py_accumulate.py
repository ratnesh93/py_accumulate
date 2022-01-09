import requests
import json
from .exception import ServerError

ENDPOINT = "https://testnet.accumulatenetwork.io/v1"
URL_acc = "acc://d4c8d9ab07daeecf50a7c78ff03c6524d941299e5601e578/ACME"
URL_adi = "acc://RedWagon"
URL_token = "acc://ACME"
HASH = "327912a9a0e9ef7916d358bc9cd5f4944adfdb168a2b017435e27a022c867ef7"
URL_keypage = "acc://testadi1/keypage1"
URL_keybook = "acc://testadi1/keybook1"

JSONRPC_VERSION = "2.0"

class BaseClass:
    def generate_payload(
        self, id, method: str, jsonrpc_version: str = JSONRPC_VERSION, params: dict() = None
    ):
        payload = {
            "jsonrpc": JSONRPC_VERSION,
            "id": id,
            "method": method,
        }
        if params:
            payload["params"] = params
        return payload
    
    def handle_response(self,res):
        res_text = json.loads(res.text)
        error_obj = res_text.get("error")
        if error_obj:
            error_obj.update({"id": res_text.get("id")})
            raise ServerError(error_obj)
        return res_text.get("result")
    
    def get_headers(self):
        return {"content-type": "application/json"}

class Accumulate(BaseClass):
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
        self.adi_class = Adi(self.endpoint)
        self.token_class = Token(self.endpoint)
        self.key_class = Key(self.endpoint)
        super().__init__()

    def __id__(self):
        self.id += 1
        return self.id

    def version(self):
        method = "version"
        payload = self.generate_payload(id=self.__id__(),method=method)
        headers = self.get_headers()
        res = requests.post(
            url=self.endpoint, headers=headers, data=json.dumps(payload)
        )
        return self.handle_response(res)

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

        Raises:
            ServerError: When request fails
        """
        params = {"url": url}
        method = "get"
        payload = self.generate_payload(id=self.__id__(), method=method, params=params)
        headers = self.get_headers()
        res = requests.post(
            url=self.endpoint, headers=headers, data=json.dumps(payload)
        )
        return self.handle_response(res)
    
    def adi(self,url: str):
        """
        Returns information about the specified ADI

        Args:
            url: The ADI URL to check

        Returns:
            url: The URL for this ADI
            publicKeyHash: The SHA-256 hash of the Public Key for this ADI

        Raises:
            -32901: Invalid ADI URL
            -32902: ADI does not exist
        """
        return self.adi_class.adi(url,self.__id__())

    def token(self,url: str):
        """
        Returns information about the specified token

        Args:
            url: Token URL

        Returns:
            token: The requested token info

        Raises:
            -33001: Invalid token URL
            -33002: Token does not exist
        """
        return self.token_class.token(url, self.__id__())

    def token_account(self,url:str):
        """
        Returns information about the specified token account

        Args:
            url: Token Account URL

        Returns:
            tokenAccountWithBalance: Token account with balance

        Raises:
            -34001: Invalid token account URL
            -34002: Token account does not exist
        """
        return self.token_class.token_account(url,self.__id__())

    def token_account_history(self, url: str):
        """
        Returns account history for the specified token account

        Args:
            url: Token Account URL

        Returns:
            tokenTxWithHash: Token transaction

        Raises:
            -34001: Invalid token account URL
            -34002: Token account does not exist
        """
        return self.token_class.token_account_history(url,self.__id__())

    def token_tx(self, hash: str):
        """
        Returns transaction data for the specified transaction

        Args:
            hash: Transaction hash

        Returns:
            tokenTxWithHash: Token transaction

        Raises:
            -34002: Invalid transaction hash
            -34003: Transaction does not exist
        """
        return self.token_class.token_tx(hash,self.__id__())

    def faucet(self, url: str):
        """
        Get free ACME tokens. While supplies last!

        Args:
            url: Token account URL

        Returns:
            txid: The transasction ID
            hash:
            codespace:
        """
        return self.token_class.faucet(url,self.__id__())

    def keypage(self, url: str):
        """
        Returns the specified key page / signature specification

        Args:
            url: Accumulate Key Page URL

        Returns:
            keyPage: An object containing the Chain URL, Key book ID, credit balance, and an unordered set of keys
        """
        return self.key_class.keypage(url,self.__id__())

    def keybook(self, url: str):
        """
        Returns information about the specified key book / Signature specification group

        Args:
            url: Accumulate key book URL

        Returns:
            keyBook: Object containing the chain URL and key page IDs
        """
        return self.key_class.keybook(url,self.__id__())


class Adi(BaseClass):
    def __init__(self,endpoint):
        self.endpoint = endpoint
        super().__init__()
        
    def adi(self, url: str,id):
        params = {"url": url}
        method = "adi"
        payload = self.generate_payload(id=id, method=method, params=params)
        headers = self.get_headers()
        res = requests.post(
            url=self.endpoint, headers=headers, data=json.dumps(payload)
        )
        return self.handle_response(res)


class Token(BaseClass):
    def __init__(self,endpoint):
        self.endpoint = endpoint
        super().__init__()

    def token(self, url: str,id):
        params = {"url": url}
        method = "token"
        payload = self.generate_payload(id=id, method=method, params=params)
        headers = self.get_headers()
        res = requests.post(
            url=self.endpoint, headers=headers, data=json.dumps(payload)
        )
        return self.handle_response(res)

    def token_account(self, url: str,id):
        params = {"url": url}
        method = "token-account"
        payload = self.generate_payload(id=id, method=method, params=params)
        headers = self.get_headers()
        res = requests.post(
            url=self.endpoint, headers=headers, data=json.dumps(payload)
        )
        return self.handle_response(res)

    def token_account_history(self, url: str,id):
        params = {"url": url}
        method = "token-account-history"
        payload = self.generate_payload(id=id, method=method, params=params)
        headers = self.get_headers()
        res = requests.post(
            url=self.endpoint, headers=headers, data=json.dumps(payload)
        )
        return self.handle_response(res)

    def token_tx(self, hash: str,id):
        params = {"hash": hash}
        method = "token-tx"
        payload = self.generate_payload(id=id, method=method, params=params)
        headers = self.get_headers()
        res = requests.post(
            url=self.endpoint, headers=headers, data=json.dumps(payload)
        )
        return self.handle_response(res)

    def faucet(self, url: str,id):
        params = {"url": url}
        method = "faucet"
        payload = self.generate_payload(id=id, method=method, params=params)
        headers = self.get_headers()
        res = requests.post(
            url=self.endpoint, headers=headers, data=json.dumps(payload)
        )
        return self.handle_response(res)        


class Key(BaseClass):

    def __init__(self,endpoint):
        self.endpoint = endpoint
        super().__init__()

    def keypage(self, url: str,id):
        params = {"url": url}
        method = "sig-spec" #TODO: name change
        payload = self.generate_payload(id=id, method=method, params=params)
        headers = self.get_headers()
        res = requests.post(
            url=self.endpoint, headers=headers, data=json.dumps(payload)
        )
        return self.handle_response(res)    

    def keybook(self, url: str,id):
        params = {"url": url}
        method = "sig-spec-group"  #TODO: name change
        payload = self.generate_payload(id=id, method=method, params=params)
        headers = self.get_headers()
        res = requests.post(
            url=self.endpoint, headers=headers, data=json.dumps(payload)
        )
        return self.handle_response(res)   

