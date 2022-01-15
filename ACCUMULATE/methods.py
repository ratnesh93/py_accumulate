import requests
import json

from .exception import ServerError
from .constants import ACCUMULATE_METHODS
from .models import (
    QueryResponse,
    QueryMultiResponse,
    AcmeFaucet,
    TxResponse,
)

JSONRPC_VERSION = "2.0"


class BaseClass:
    def generate_payload(
        self,
        id,
        method: str,
        jsonrpc_version: str = JSONRPC_VERSION,
        params: dict() = None,
    ):
        payload = {
            "jsonrpc": jsonrpc_version,
            "id": id,
            "method": method,
        }
        if params:
            payload["params"] = params
        return payload

    def handle_response(self, res):
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
        self.token_class = Token(self.endpoint)
        self.url_method_class = URL_Methods(self.endpoint)
        self.keyManagementMethods = KeyManagementMethods(self.endpoint)
        self.executeMethods = ExecuteMethods(self.endpoint)
        super().__init__()

    def __id__(self):
        self.id += 1
        return self.id

    def Version(self):
        """
        returns QueryResponse with VersionResponse
        """
        method = ACCUMULATE_METHODS.VERSION
        payload = self.generate_payload(id=self.__id__(), method=method)
        headers = self.get_headers()
        res = requests.post(
            url=self.endpoint, headers=headers, data=json.dumps(payload)
        )
        result = self.handle_response(res)
        queryResponse = QueryResponse(**result)
        return queryResponse

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
        return self.url_method_class.Query(self.__id__(), url)

    def QueryTxHistory(self, url: str, count, start=None):
        """
        Input:  TxHistoryQuery:
                    non-binary: true
                    incomparable: true
                    embeddings:
                    - UrlQuery
                    - QueryPagination

        QueryPagination:
            non-binary: true
            incomparable: true
            fields:
            - name: Start
                type: uvarint
                optional: true
            - name: Count
                type: uvarint
                optional: true
        """
        return self.url_method_class.QueryTxHistory(
            self.__id__(), url, count=count, start=start
        )

    def QueryTx(self, txid, wait=None):
        """
        Returns transaction data for the specified transaction
        input:  TxnQuery:
                    non-binary: true
                    incomparable: true
                    fields:
                    - name: Txid
                        type: bytes
                    - name: Wait
                        type: duration
                        optional: true

        """
        return self.url_method_class.QueryTx(self.__id__(), txid, wait)

    def QueryChain(self, chainId):
        """
        Get query-chain properties
        input: ChainIdQuery:
                    non-binary: true
                    incomparable: true
                    fields:
                    - name: ChainId
                        type: bytes
        """
        return self.url_method_class.QueryChain(self.__id__(), chainId)

    def QueryData(self, url, entryHash=None):
        """
        input:  DataEntryQuery:
                    fields:
                        - name: Url
                            type: string
                            is-url: true
                        - name: EntryHash
                            type: chain
                            optional: true
        """
        return self.url_method_class.QueryData(self.__id__(), url, entryHash)

    def QueryKeyPageIndex(self, url, key=None):
        """
        input:  KeyPageIndexQuery:
                    non-binary: true
                    incomparable: true
                    embeddings:
                    - UrlQuery
                    fields:
                    - name: Key
                        type: bytes
        """
        return self.keyManagementMethods.QueryKeyPageIndex(self.__id__(), url, key)

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
        return self.token_class.Faucet(self.__id__(), url)

    def QueryDirectory(self, url: str, count=None, start=None, expandChains=None):
        """
        input:  DirectoryQuery:
                    non-binary: true
                    incomparable: true
                    embeddings:
                        - UrlQuery
                        - QueryPagination
                        - QueryOptions
        QueryPagination:
            non-binary: true
            incomparable: true
            fields:
            - name: Start
                type: uvarint
                optional: true
            - name: Count
                type: uvarint
                optional: true
        QueryOptions:
            non-binary: true
            incomparable: true
            fields:
            - name: ExpandChains
                type: bool
                optional: true
        """
        self.url_method_class.QueryDirectory(
            self.__id__(), url, count=count, start=start, expandChains=expandChains
        )

    def QueryDataSet(self, url: str, queryPagination, queryOptions):
        """
        input:  DataEntrySetQuery:
                    non-binary: true
                    incomparable: true
                    embeddings:
                        - UrlQuery
                        - QueryPagination
                        - QueryOptions
        """
        self.url_method_class.QueryDataSet(
            self.__id__(), url, queryPagination, queryOptions
        )

    def Execute(self, sponsor, signer, signature, keyPage, payload, checkOnly=None):
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
        self.executeMethods.Execute(
            self.__id__(),
            sponsor=sponsor,
            signer=signer,
            signature=signature,
            keyPage=keyPage,
            payload=payload,
            checkOnly=checkOnly,
        )

    def ExecuteCreateAdi(self, url, publicKey, keyBookName=None, keyPageName=None):
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
        self.executeMethods.ExecuteCreateAdi(
            self.__id__(),
            url,
            publicKey=publicKey,
            keyBookName=keyBookName,
            KeyPageName=keyPageName,
        )

    def ExecuteCreateDataAccount(self, url, keyBookUrl=None, managerKeyBookUrl=None):
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
        self.executeMethods.ExecuteCreateDataAccount(
            self.__id__(),
            url,
            KeyBookUrl=keyBookUrl,
            ManagerKeyBookUrl=managerKeyBookUrl,
        )

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

    def ExecuteCreateToken(self, url, Symbol, Precision, Properties=None):
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
        self.executeMethods.ExecuteCreateToken(
            self.__id__(),
            url=url,
            Symbol=Symbol,
            Precision=Precision,
            Properties=Properties,
        )

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
        self.executeMethods.ExecuteCreateTokenAccount(
            self.__id__(), url, TokenUrl=TokenUrl, KeyBookUrl=KeyBookUrl
        )

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
        self.executeMethods.ExecuteSendTokens(self.__id(), To, Hash=Hash, Meta=Meta)

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
        self.executeMethods.ExecuteUpdateKeyPage(
            self.__id__(), Operation, Key=Key, NewKey=NewKey, Owner=Owner
        )

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

    def Metrics(self, metric: str, duration):
        """
        input:
            metric,  example = "tps"
            duration,  example = "1h"
        """
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


class URL_Methods(BaseClass):
    def __init__(self, endpoint):
        self.endpoint = endpoint
        super().__init__()

    def Query(self, id, url: str):
        params = {"url": url}
        method = ACCUMULATE_METHODS.Query
        payload = self.generate_payload(id=id, method=method, params=params)
        headers = self.get_headers()
        res = requests.post(
            url=self.endpoint, headers=headers, data=json.dumps(payload)
        )
        result = self.handle_response(res)
        queryResponse = QueryResponse(**result)
        return queryResponse

    def QueryTxHistory(self, id, url: str, count, start=None):
        params = {"url": url, "count": count}
        if start:
            params.update({"start": start})
        method = ACCUMULATE_METHODS.QueryTxHistory
        payload = self.generate_payload(id=id, method=method, params=params)
        headers = self.get_headers()
        res = requests.post(
            url=self.endpoint, headers=headers, data=json.dumps(payload)
        )
        result = self.handle_response(res)
        queryMultiResponse = QueryMultiResponse(**result)
        return queryMultiResponse

    def QueryTx(self, id, txId, wait=None):
        params = {"txid": txId}
        if wait:
            params.update({"wait": wait})
        method = ACCUMULATE_METHODS.QueryTx
        payload = self.generate_payload(id=id, method=method, params=params)
        headers = self.get_headers()
        res = requests.post(
            url=self.endpoint, headers=headers, data=json.dumps(payload)
        )
        result = self.handle_response(res)
        acmeFaucet = AcmeFaucet(**result)
        return acmeFaucet

    def QueryChain(self, id, chainId):
        params = {"chainId": chainId}
        method = ACCUMULATE_METHODS.QueryChain
        payload = self.generate_payload(id=id, method=method, params=params)
        headers = self.get_headers()
        res = requests.post(
            url=self.endpoint, headers=headers, data=json.dumps(payload)
        )
        result = self.handle_response(res)
        queryResponse = QueryResponse(**result)
        return queryResponse

    def QueryData(self, id, url, entryHash=None):
        params = {"url": url}
        if entryHash:
            params.update({"entryHash": entryHash})
        method = ACCUMULATE_METHODS.QueryData
        payload = self.generate_payload(id=id, method=method, params=params)
        headers = self.get_headers()
        res = requests.post(
            url=self.endpoint, headers=headers, data=json.dumps(payload)
        )
        result = self.handle_response(res)
        queryResponse = QueryResponse(**result)
        return queryResponse

    def QueryDataSet(self, id, url: str, queryPagination, queryOptions):
        params = {"url": url}
        if queryPagination:
            params.update({"queryPagination": queryPagination})
        if queryOptions:
            params.update({"queryOptions": queryOptions})
        method = ACCUMULATE_METHODS.QueryDataSet
        payload = self.generate_payload(id=id, method=method, params=params)
        headers = self.get_headers()
        res = requests.post(
            url=self.endpoint, headers=headers, data=json.dumps(payload)
        )
        result = self.handle_response(res)
        queryMultiResponse = QueryMultiResponse(**result)
        return queryMultiResponse

    def QueryDirectory(self, id, url: str, count=None, start=None, expandChains=None):
        params = {"url": url}
        if count:
            params.update({"count": count})
        if start:
            params.update({"start": start})
        if expandChains:
            params.update({"expandChains": expandChains})
        method = ACCUMULATE_METHODS.QueryDirectory
        payload = self.generate_payload(id=id, method=method, params=params)
        headers = self.get_headers()
        res = requests.post(
            url=self.endpoint, headers=headers, data=json.dumps(payload)
        )
        result = self.handle_response(res)
        queryMultiResponse = QueryMultiResponse(**result)
        return queryMultiResponse


class Token(BaseClass):
    def __init__(self, endpoint):
        self.endpoint = endpoint
        super().__init__()

    def Faucet(self, id, url: str):
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


class KeyManagementMethods(BaseClass):
    def __init__(self, endpoint):
        self.endpoint = endpoint
        super().__init__()

    def QueryKeyPageIndex(id, self, url, key):
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
    def __init__(self, endpoint):
        self.endpoint = endpoint
        super().__init__()

    def Execute(self, id, sponsor, signer, signature, keyPage, payload, checkOnly=None):
        params = {
            "sponsor": sponsor,
            "signer": signer,
            "signature": signature,
            "keyPage": keyPage,
            "payload": payload,
        }
        if checkOnly:
            params.update({"checkOnly": checkOnly})
        method = ACCUMULATE_METHODS.Execute
        payload = self.generate_payload(id=id, method=method, params=params)
        headers = self.get_headers()
        res = requests.post(
            url=self.endpoint, headers=headers, data=json.dumps(payload)
        )
        result = self.handle_response(res)
        txResponse = TxResponse(**result)
        return txResponse

    def ExecuteCreateAdi(self, id, url, publicKey, keyBookName=None, keyPageName=None):
        params = {"url": url, "publicKey": publicKey}
        if keyBookName:
            params.update({"keyBookName": keyBookName})
        if keyPageName:
            params.update({"keyPageName": keyPageName})
        method = ACCUMULATE_METHODS.ExecuteCreateAdi
        payload = self.generate_payload(id=id, method=method, params=params)
        headers = self.get_headers()
        res = requests.post(
            url=self.endpoint, headers=headers, data=json.dumps(payload)
        )
        result = self.handle_response(res)
        return result

    def ExecuteCreateDataAccount(
        self, id, url, KeyBookUrl=None, ManagerKeyBookUrl=None
    ):
        params = {"url": url}
        if KeyBookUrl:
            params.update({"KeyBookUrl": KeyBookUrl})
        if ManagerKeyBookUrl:
            params.update({"ManagerKeyBookUrl": ManagerKeyBookUrl})
        method = ACCUMULATE_METHODS.ExecuteCreateDataAccount
        payload = self.generate_payload(id=id, method=method, params=params)
        headers = self.get_headers()
        res = requests.post(
            url=self.endpoint, headers=headers, data=json.dumps(payload)
        )
        result = self.handle_response(res)
        return result

    def ExecuteCreateKeyBook(self, id, url, Pages):
        params = {"url": url, "Pages": Pages}
        method = ACCUMULATE_METHODS.ExecuteCreateKeyBook
        payload = self.generate_payload(id=id, method=method, params=params)
        headers = self.get_headers()
        res = requests.post(
            url=self.endpoint, headers=headers, data=json.dumps(payload)
        )
        result = self.handle_response(res)
        return result

    def ExecuteCreateKeyPage(self, id, url, Keys):
        params = {"url": url, "Keys": Keys}
        method = ACCUMULATE_METHODS.ExecuteCreateKeyPage
        payload = self.generate_payload(id=id, method=method, params=params)
        headers = self.get_headers()
        res = requests.post(
            url=self.endpoint, headers=headers, data=json.dumps(payload)
        )
        result = self.handle_response(res)
        return result

    def ExecuteCreateToken(self, id, url, Symbol, Precision, Properties=None):
        params = {"url": url, "Symbol": Symbol, "Precision": Precision}
        if Properties:
            params.update({"Properties": Properties})
        method = ACCUMULATE_METHODS.ExecuteCreateToken
        payload = self.generate_payload(id=id, method=method, params=params)
        headers = self.get_headers()
        res = requests.post(
            url=self.endpoint, headers=headers, data=json.dumps(payload)
        )
        result = self.handle_response(res)
        return result

    def ExecuteCreateTokenAccount(self, id, url, TokenUrl, KeyBookUrl):
        params = {"url": url, "TokenUrl": TokenUrl, "KeyBookUrl": KeyBookUrl}
        method = ACCUMULATE_METHODS.ExecuteCreateTokenAccount
        payload = self.generate_payload(id=id, method=method, params=params)
        headers = self.get_headers()
        res = requests.post(
            url=self.endpoint, headers=headers, data=json.dumps(payload)
        )
        result = self.handle_response(res)
        return result

    def ExecuteSendTokens(self, id, To, Hash=None, Meta=None):
        params = {"To": To}
        if Hash:
            params.update({"Hash": Hash})
        if Meta:
            params.update({"Meta": Meta})
        method = ACCUMULATE_METHODS.ExecuteSendTokens
        payload = self.generate_payload(id=id, method=method, params=params)
        headers = self.get_headers()
        res = requests.post(
            url=self.endpoint, headers=headers, data=json.dumps(payload)
        )
        result = self.handle_response(res)
        return result

    def ExecuteAddCredits(self, id, Recipient, Amount):
        params = {"Recipient": Recipient, "Amount": Amount}
        method = ACCUMULATE_METHODS.ExecuteAddCredits
        payload = self.generate_payload(id=id, method=method, params=params)
        headers = self.get_headers()
        res = requests.post(
            url=self.endpoint, headers=headers, data=json.dumps(payload)
        )
        result = self.handle_response(res)
        return result

    def ExecuteUpdateKeyPage(self, id, Operation, Key=None, NewKey=None, Owner=None):
        params = {"Operation": Operation}
        if Key:
            params.update({"Key": Key})
        if NewKey:
            params.update({"NewKey": NewKey})
        if Owner:
            params.update({"Owner": Owner})
        method = ACCUMULATE_METHODS.ExecuteUpdateKeyPage
        payload = self.generate_payload(id=id, method=method, params=params)
        headers = self.get_headers()
        res = requests.post(
            url=self.endpoint, headers=headers, data=json.dumps(payload)
        )
        result = self.handle_response(res)
        return result

    def ExecuteWriteData(self, id, Entry):
        params = {"Entry": Entry}
        method = ACCUMULATE_METHODS.ExecuteWriteData
        payload = self.generate_payload(id=id, method=method, params=params)
        headers = self.get_headers()
        res = requests.post(
            url=self.endpoint, headers=headers, data=json.dumps(payload)
        )
        result = self.handle_response(res)
        return result
