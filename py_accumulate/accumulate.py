import requests
import json

from requests.sessions import RecentlyUsedContainer
from exception import ServerError
from constants import ACCUMULATE_METHODS
from models import VersionResponse, QueryResponse, QueryMultiResponse, AcmeFaucet, TxResponse, MetricsResponse

ENDPOINT = "https://testnet.accumulatenetwork.io/v2"
URL_acc = "acc://d4c8d9ab07daeecf50a7c78ff03c6524d941299e5601e578/ACME"
URL_adi = "acc://RedWagon"
URL_token = "acc://ACME"
ADI = "adione"
HASH = "327912a9a0e9ef7916d358bc9cd5f4944adfdb168a2b017435e27a022c867ef7"
URL_keypage = "acc://testadi1/keypage1"
URL_keybook = "acc://testadi1/keybook1"
TXID = "9dce91ec75f5b5e767283d8db77394daeef6e50b4f0e1197624f1a888ed076b1"
CHAIN_ID= "12e2d2d82f7b65752b3fd8d37d195f6d87f6cb24b83c4ae70f4571ea1007e741"
URL_QUERY_DATA = "acc://aditwo/aditwodata"
ENTRY_HASH = "b45fa53718dbc5bf31f2f6134d1ff84fe22b3760face9c2ab012fd66d16d1808"
URL_PAGE = "acc://adione/page0"
KEY = {
        "publicKey": "57ddf8f09ddaaf28656fcca6ef1d4bb028c02ed31584c36df1e0ffcacc14d90c"
    }
PUBLIC_KEY = "57ddf8f09ddaaf28656fcca6ef1d4bb028c02ed31584c36df1e0ffcacc14d90c"

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
        self.url_method_class = URL_Methods(self.endpoint)
        self.keyManagementMethods = KeyManagementMethods(self.endpoint)
        self.executeMethods= ExecuteMethods(self.endpoint)
        super().__init__()

    def __id__(self):
        self.id += 1
        return self.id

    def Version(self):
        method = ACCUMULATE_METHODS.VERSION
        payload = self.generate_payload(id=self.__id__(),method=method)
        headers = self.get_headers()
        res = requests.post(
            url=self.endpoint, headers=headers, data=json.dumps(payload)
        )
        result = self.handle_response(res)
        versionResponse = VersionResponse(**result)
        return versionResponse

    def Query(self, url: str):
        """
        Returns Accumulate Object by URL
        Args:
            url: Any Accumulate URL

        Returns:
            type: The Accumulate object type
            merkleState
            data: The data for this object (properties vary)
        """
        return self.url_method_class.Query(url,self.__id__())
    
    def QueryTxHistory(self, url: str, count, start = None):
        return self.url_method_class.QueryTxHistory(url, count,self.__id__(), start)
    
    
    def QueryTx(self, txid, wait= None):
        return self.url_method_class.QueryTx(txid, self.__id__(), wait)
    
    def QueryChain(self, chainId):
        return self.url_method_class.QueryChain(chainId, self.__id__())

    def QueryData(self, url, entryHash= None):
        return self.url_method_class.QueryData(url, self.__id__(), entryHash)

    def QueryKeyPageIndex(self, url, key = None):
        return self.keyManagementMethods.QueryKeyPageIndex(url, self.__id__(), key)
    
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

    def Faucet(self, url: str):
        """
        Get free ACME tokens. While supplies last!

        Args:
            url: Token account URL

        Returns:
            txid: The transasction ID
            hash:
            codespace:
        """
        return self.token_class.Faucet(url,self.__id__())

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
    
    def QueryDirectory(self, url: str, queryPagination, queryOptions):
        self.url_method_class.QueryDirectory(url, self.__id__(), queryPagination, queryOptions)
    
    def QueryDataSet(self, url: str, queryPagination, queryOptions):
        self.url_method_class.QueryDataSet(url, self.__id__(), queryPagination, queryOptions)

    def execute(self, sponsor, signer, signature, keyPage, payload, checkOnly= None):
        """
        input: TxRequest:
                    non-binary: true
                    incomparable: true
                    fields:
                    - name: CheckOnly
                        type: bool
                        optional: true
                    - name: Origin
                        type: url.URL
                        marshal-as: reference
                        pointer: true
                        alternative: Sponsor
                    - name: Signer
                        type: Signer
                        marshal-as: reference
                    - name: Signature
                        type: bytes
                    - name: KeyPage
                        type: KeyPage
                        marshal-as: reference
                    - name: Payload
                        type: any
        """
        self.executeMethods.Execute(self.__id__(), sponsor, signer, signature, keyPage, payload, checkOnly= checkOnly)
    
    def ExecuteCreateAdi(self, url, publicKey, keyBookName = None, keyPageName = None):
        """
        input: CreateIdentity:
                    kind: tx
                    fields:
                        - name: Url
                            type: string
                            is-url: true
                        - name: PublicKey
                            type: bytes
                        - name: KeyBookName
                            type: string
                            optional: true
                        - name: KeyPageName
                            type: string
                            optional: true
        """
        self.executeMethods.ExecuteCreateAdi(self.__id__(), url, publicKey, keyBookName = keyBookName, KeyPageName = keyPageName)
    
    def ExecuteCreateDataAccount(self, url, KeyBookUrl=None, ManagerKeyBookUrl=None):
        """
        input: CreateDataAccount:
                    kind: tx
                    fields:
                        - name: Url
                            type: string
                            is-url: true
                        - name: KeyBookUrl
                            type: string
                            is-url: true
                            optional: true
                        - name: ManagerKeyBookUrl
                            type: string
                            is-url: true
                            optional: true
        """
        self.executeMethods.ExecuteCreateDataAccount(self.__id__(), url, KeyBookUrl, ManagerKeyBookUrl)

    def ExecuteCreateKeyBook(self, url, Pages):
        """
        input: CreateKeyBook:
                    kind: tx
                    fields:
                        - name: Url
                            type: string
                            is-url: true
                        - name: Pages
                            type: slice
                            slice:
                                type: string
                                is-url: true
        """
        self.executeMethods.ExecuteCreateKeyBook(self.__id__(), url, Pages)

    def ExecuteCreateKeyPage(self, url, Keys):
        """
        input:  CreateKeyPage:
                    kind: tx
                    fields:
                        - name: Url
                            type: string
                            is-url: true
                        - name: Keys
                            type: slice
                            slice:
                                type: KeySpecParams
                                pointer: true
                                marshal-as: reference
        """
        self.executeMethods.ExecuteCreateKeyPage(self.__id__(), url, Keys)

    def ExecuteCreateToken(self, url, Symbol, Precision, Properties= None):
        """
        input:  CreateToken:
                    kind: tx
                    fields:
                        - name: Url
                            type: string
                            is-url: true
                        - name: Symbol
                            type: string
                        - name: Precision
                            type: uvarint
                        - name: Properties
                            type: string
                            is-url: true
                            optional: true
        """
        self.executeMethods.ExecuteCreateToken(self.__id__(), url, Symbol, Precision, Properties)

    def ExecuteCreateTokenAccount(self, url, TokenUrl, KeyBookUrl):
        """
        input: CreateTokenAccount:
                    kind: tx
                    fields:
                        - name: Url
                            type: string
                            is-url: true
                        - name: TokenUrl
                            type: string
                            is-url: true
                        - name: KeyBookUrl
                            type: string
                            is-url: true
        """
        self.executeMethods.ExecuteCreateTokenAccount(self.__id__(), url, TokenUrl, KeyBookUrl)

    def ExecuteSendTokens(self, To, Hash=None, Meta=None):
        """
        input: SendTokens:
                    kind: tx
                    fields:
                        - name: Hash
                            type: chain
                            optional: true
                        - name: Meta
                            type: rawJson
                            optional: true
                        - name: To
                            type: slice
                            slice:
                                type: TokenRecipient
                                marshal-as: reference
                                pointer: true
        """
        self.executeMethods.ExecuteSendTokens(self.__id(), To, Hash = Hash, Meta = Meta)

    def ExecuteAddCredits(self, Recipient, Amount):
        """
        input: AddCredits:
                    kind: tx
                    fields:
                        - name: Recipient
                            type: string
                        - name: Amount
                            type: uvarint
        """
        self.executeMethods.ExecuteAddCredits(self.__id__(), Recipient, Amount)

    def ExecuteUpdateKeyPage(self, Operation, Key=None, NewKey=None, Owner=None):
        """
        input: UpdateKeyPage:
                    kind: tx
                    fields:
                        - name: Operation
                            type: KeyPageOperation
                            marshal-as: value
                        - name: Key
                            type: bytes
                            optional: true
                        - name: NewKey
                            type: bytes
                            optional: true
                        - name: Owner
                            type: string
                            optional: true
        """
        self.executeMethods.ExecuteUpdateKeyPage(self.__id__(), Operation, Key= Key, NewKey= NewKey, Owner= Owner)

    def ExecuteWriteData(self, Entry):
        """
        input: WriteData:
                    kind: tx
                    fields:
                        - name: Entry
                            type: DataEntry
                            marshal-as: reference
        """
        self.executeMethods.ExecuteWriteData(self.__id__(), Entry)
    
    def Metrics(self, metric:str, duration):
        params = {"metric": metric, "duration": duration}
        method = ACCUMULATE_METHODS.Metrics
        payload = self.generate_payload(id=self.__id__(), method=method, params=params)
        headers = self.get_headers()
        res = requests.post(
            url=self.endpoint, headers=headers, data=json.dumps(payload)
        )
        result = self.handle_response(res)
        queryResponse = QueryResponse(**result)
        return queryResponse


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

class URL_Methods(BaseClass):
    def __init__(self,endpoint):
        self.endpoint = endpoint
        super().__init__()
        
    def Query(self, url: str,id):
        params = {"url": url}
        method = ACCUMULATE_METHODS.Query
        payload = self.generate_payload(id=id, method=method, params=params)
        headers = self.get_headers()
        res = requests.post(
            url=self.endpoint, headers=headers, data=json.dumps(payload)
        )
        result =  self.handle_response(res)
        queryResponse = QueryResponse(**result)
        return queryResponse
    
    def QueryTxHistory(self,url: str, count, id, start= None):
        params = {"url": url, "count":count}
        if start:
            params.update({"start":start})
        method = ACCUMULATE_METHODS.QueryTxHistory
        payload = self.generate_payload(id=id, method=method, params=params)
        headers = self.get_headers()
        res = requests.post(
            url=self.endpoint, headers=headers, data=json.dumps(payload)
        )
        result =  self.handle_response(res)
        queryMultiResponse = QueryMultiResponse(**result)
        return queryMultiResponse

    def QueryTx(self, txId, id, wait= None):
        params = {"txid": txId}
        if wait:
            params.update({"wait":wait})
        method = ACCUMULATE_METHODS.QueryTx
        payload = self.generate_payload(id=id, method=method, params=params)
        headers = self.get_headers()
        res = requests.post(
            url=self.endpoint, headers=headers, data=json.dumps(payload)
        )
        result =  self.handle_response(res)
        acmeFaucet = AcmeFaucet(**result)
        return acmeFaucet
    
    def QueryChain(self, chainId, id):
        params = {"chainId": chainId}
        method = ACCUMULATE_METHODS.QueryChain
        payload = self.generate_payload(id=id, method=method, params=params)
        headers = self.get_headers()
        res = requests.post(
            url=self.endpoint, headers=headers, data=json.dumps(payload)
        )
        result =  self.handle_response(res)
        queryResponse = QueryResponse(**result)
        return queryResponse
    
    def QueryData(self, url, id, entryHash= None):
        params = {"url": url}
        if entryHash:
            params.update({"entryHash":entryHash})
        method = ACCUMULATE_METHODS.QueryData
        payload = self.generate_payload(id=id, method=method, params=params)
        headers = self.get_headers()
        res = requests.post(
            url=self.endpoint, headers=headers, data=json.dumps(payload)
        )
        result =  self.handle_response(res)
        queryResponse = QueryResponse(**result)
        return queryResponse
    
    def QueryDataSet(self, url: str,id, queryPagination, queryOptions):
        params = {"url": url}
        if queryPagination:
            params.update({"queryPagination":queryPagination})
        if queryOptions:
            params.update({"queryOptions":queryOptions})
        method = ACCUMULATE_METHODS.QueryDataSet
        payload = self.generate_payload(id=id, method=method, params=params)
        headers = self.get_headers()
        res = requests.post(
            url=self.endpoint, headers=headers, data=json.dumps(payload)
        )
        result =  self.handle_response(res)
        queryMultiResponse = QueryMultiResponse(**result)
        return queryMultiResponse
    
    def QueryDirectory(self, url: str,id, queryPagination, queryOptions):
        params = {"url": url}
        if queryPagination:
            params.update({"queryPagination":queryPagination})
        if queryOptions:
            params.update({"queryOptions":queryOptions})
        method = ACCUMULATE_METHODS.QueryDirectory
        payload = self.generate_payload(id=id, method=method, params=params)
        headers = self.get_headers()
        res = requests.post(
            url=self.endpoint, headers=headers, data=json.dumps(payload)
        )
        result =  self.handle_response(res)
        queryMultiResponse = QueryMultiResponse(**result)
        return queryMultiResponse

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

    def Faucet(self, url: str, id):
        params = {"url": url}
        method = ACCUMULATE_METHODS.Faucet
        payload = self.generate_payload(id=id, method=method, params=params)
        headers = self.get_headers()
        res = requests.post(
            url=self.endpoint, headers=headers, data=json.dumps(payload)
        )
        result = self.handle_response(res)        
        txResponse = TxResponse(**result)
        return txResponse

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


class KeyManagementMethods(BaseClass):
    def __init__(self,endpoint):
        self.endpoint = endpoint
        super().__init__()
    
    def QueryKeyPageIndex(self, url, id, key):
        params = {"url": url, "key": key}
        method = ACCUMULATE_METHODS.QueryKeyPageIndex
        payload = self.generate_payload(id=id, method=method, params=params)
        headers = self.get_headers()
        res = requests.post(
            url=self.endpoint, headers=headers, data=json.dumps(payload)
        )
        result = self.handle_response(res)
        queryResponse = QueryResponse(**result)
        return queryResponse

class ExecuteMethods(BaseClass):
    
    def __init__(self,endpoint):
        self.endpoint = endpoint
        super().__init__()
    
    def Execute(self, id, sponsor, signer, signature, keyPage, payload, checkOnly= None):
        params = {
            "sponsor": sponsor,
            "signer": signer,
            "signature": signature,
            "keyPage": keyPage,
            "payload": payload
        }
        if checkOnly:
            params.update({"checkOnly":checkOnly})
        method = ACCUMULATE_METHODS.Execute
        payload = self.generate_payload(id=id, method=method, params=params)
        headers = self.get_headers()
        res = requests.post(
            url=self.endpoint, headers=headers, data=json.dumps(payload)
        )
        result = self.handle_response(res)
        txResponse = TxResponse(**result)
        return txResponse

    def ExecuteCreateAdi(self, id, url, publicKey, keyBookName = None, keyPageName = None):
        params = {
            "url": url,
            "publicKey":publicKey
        }
        if keyBookName:
            params.update({"keyBookName":keyBookName})
        if keyPageName:
            params.update({"keyPageName":keyPageName})
        method = ACCUMULATE_METHODS.ExecuteCreateAdi
        payload = self.generate_payload(id=id, method=method, params=params)
        headers = self.get_headers()
        res = requests.post(
            url=self.endpoint, headers=headers, data=json.dumps(payload)
        )
        result = self.handle_response(res)
        return result
    
    def ExecuteCreateDataAccount(self, id, url, KeyBookUrl=None, ManagerKeyBookUrl=None):
        params = {
            "url": url
        }
        if KeyBookUrl:
            params.update({"KeyBookUrl":KeyBookUrl})
        if ManagerKeyBookUrl:
            params.update({"ManagerKeyBookUrl":ManagerKeyBookUrl})
        method = ACCUMULATE_METHODS.ExecuteCreateDataAccount
        payload = self.generate_payload(id=id, method=method, params=params)
        headers = self.get_headers()
        res = requests.post(
            url=self.endpoint, headers=headers, data=json.dumps(payload)
        )
        result = self.handle_response(res)
        return result
    
    def ExecuteCreateKeyBook(self, id, url, Pages):
        params = {
            "url": url,
            "Pages": Pages
        }
        method = ACCUMULATE_METHODS.ExecuteCreateKeyBook
        payload = self.generate_payload(id=id, method=method, params=params)
        headers = self.get_headers()
        res = requests.post(
            url=self.endpoint, headers=headers, data=json.dumps(payload)
        )
        result = self.handle_response(res)
        return result

    def ExecuteCreateKeyPage(self, id, url, Keys):
        params = {
            "url": url,
            "Keys": Keys
        }
        method = ACCUMULATE_METHODS.ExecuteCreateKeyPage
        payload = self.generate_payload(id=id, method=method, params=params)
        headers = self.get_headers()
        res = requests.post(
            url=self.endpoint, headers=headers, data=json.dumps(payload)
        )
        result = self.handle_response(res)
        return result

    def ExecuteCreateToken(self, id, url, Symbol, Precision, Properties= None):
        params = {
            "url": url,
            "Symbol": Symbol, 
            "Precision": Precision
        }
        if Properties:
            params.update({"Properties":Properties})
        method = ACCUMULATE_METHODS.ExecuteCreateToken
        payload = self.generate_payload(id=id, method=method, params=params)
        headers = self.get_headers()
        res = requests.post(
            url=self.endpoint, headers=headers, data=json.dumps(payload)
        )
        result = self.handle_response(res)
        return result


    def ExecuteCreateTokenAccount(self, id, url, TokenUrl, KeyBookUrl):
        params = {
            "url": url,
            "TokenUrl": TokenUrl, 
            "KeyBookUrl": KeyBookUrl
        }
        method = ACCUMULATE_METHODS.ExecuteCreateTokenAccount
        payload = self.generate_payload(id=id, method=method, params=params)
        headers = self.get_headers()
        res = requests.post(
            url=self.endpoint, headers=headers, data=json.dumps(payload)
        )
        result = self.handle_response(res)
        return result

    
    def ExecuteSendTokens(self, id, To, Hash=None, Meta=None):
        params = {
            "To": To
        }
        if Hash:
            params.update({"Hash":Hash})
        if Meta:
            params.update({"Meta":Meta})
        method = ACCUMULATE_METHODS.ExecuteSendTokens
        payload = self.generate_payload(id=id, method=method, params=params)
        headers = self.get_headers()
        res = requests.post(
            url=self.endpoint, headers=headers, data=json.dumps(payload)
        )
        result = self.handle_response(res)
        return result

    def ExecuteAddCredits(self, id, Recipient, Amount):
        params = {
            "Recipient": Recipient,
            "Amount": Amount
        }
        method = ACCUMULATE_METHODS.ExecuteAddCredits
        payload = self.generate_payload(id=id, method=method, params=params)
        headers = self.get_headers()
        res = requests.post(
            url=self.endpoint, headers=headers, data=json.dumps(payload)
        )
        result = self.handle_response(res)
        return result

    def ExecuteUpdateKeyPage(self, id, Operation, Key=None, NewKey=None, Owner=None):
        params = {
            "Operation": Operation
        }
        if Key:
            params.update({"Key":Key})
        if NewKey:
            params.update({"NewKey":NewKey})
        if Owner:
            params.update({"Owner":Owner})
        method = ACCUMULATE_METHODS.ExecuteUpdateKeyPage
        payload = self.generate_payload(id=id, method=method, params=params)
        headers = self.get_headers()
        res = requests.post(
            url=self.endpoint, headers=headers, data=json.dumps(payload)
        )
        result = self.handle_response(res)
        return result

    def ExecuteWriteData(self, id, Entry):
        params = {
            "Entry": Entry
        }
        method = ACCUMULATE_METHODS.ExecuteWriteData
        payload = self.generate_payload(id=id, method=method, params=params)
        headers = self.get_headers()
        res = requests.post(
            url=self.endpoint, headers=headers, data=json.dumps(payload)
        )
        result = self.handle_response(res)
        return result



a=Accumulate(ENDPOINT)
# res = a.Query(URL_acc)
# res2= a.Query(ADI)
#res = a.QueryTxHistory(URL_acc, 2)
#res = a.QueryTxHistory(URL_acc, 2, 2)
#res = a.QueryTx(TXID)
#res = a.QueryTx(TXID, 2)
#res = a.Faucet(URL_acc)
#res = a.QueryChain(CHAIN_ID)
#res = a.QueryData(URL_QUERY_DATA)
#res = a.QueryData(URL_QUERY_DATA, ENTRY_HASH)
#res = a.QueryKeyPageIndex(URL_PAGE, PUBLIC_KEY) #: Dont write test case for it
MetricsQuery = {
    "metric":URL_acc,
    "duration": 2
}
metric =  "tps"
duration =  "1h"
res  = a.Metrics(metric, duration)
QUERY_PAGINATION = {
    "start": 1,
    "count": 2
}
QUERY_OPTIONS = {
    "ExpandChains": True
}
#res = a.QueryDirectory(URL_acc, 1,2,True)