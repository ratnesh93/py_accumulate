from .constants import ACCUMULATE_TYPES 

class Version:
    def __init__(self, commit, version, versionIsKnown):
        self.commit = commit
        self.version = version
        self.versionIsknown = versionIsKnown

class VersionResponse:
    def __init__(self, type, data):
        self.type = type
        self.version = Version(**data)

class DataEntry:
    def __init__(self, data, extIds=None):
        self.extIds = extIds
        self.data = data

class DataEntryQueryResponse:
    def __init__(self, entryHash, entry):
        self.entryHash = entryHash
        self.entry = DataEntry(**entry)


class DirectoryQueryResult:
    def __init__(self, total, entries=None, expandedEntries=None):
        self.total = total
        self.entries = entries
        self.expandedEntries = expandedEntries

class LiteTokenAccount:
    def __init__(self, type, url, keyBook, managerKeyBook, tokenUrl, balance, txCount, creditBalance):
        self.type = type
        self.url = url
        self.keyBook = keyBook
        self.managerKeyBook = managerKeyBook
        self.tokenUrl = tokenUrl
        self.balance = balance
        self.txCount = txCount
        self.creditBalance = creditBalance

class Identity:
    def __init__(self, type, url, keyBook, managerKeyBook, keyType, keyData, nonce):
        self.type = type
        self.url = url
        self.keyBook = keyBook
        self.managerKeyBook = managerKeyBook
        self.keyType = keyType
        self.keyData = keyData
        self.nonce = nonce

class MerkleState:
    def __init__(self, count, roots):
        self.count = count
        self.roots = roots

class SyntheticDepositTokens:
    def __init__(self, type, data, sponsor, keyPage, txid, signer, sig, status):
        self.type = type
        self.data = data
        self.sponsor = sponsor
        self.keyPage = keyPage
        self.txid = txid
        self.signer = signer
        self.sig = sig
        self.status = status

class KeyPage:
    def __init__(self, type, url, keyBook, managerKeyBook, creditBalance, keys):
        self.type = type
        self.url = url
        self.keyBook = keyBook
        self.managerKeyBook = managerKeyBook
        self.creditBalance = creditBalance
        self.keys = keys


class MetricsResponse:
    def __init__(self, value):
        self.value = value

class AcmeFaucet:
    def __init__(self, type, data, sponsor, keyPage, txid, signer, sig, status, syntheticTxids):
        self.type = type
        self.data = data
        self.sponsor = sponsor
        self.keyPage = keyPage
        self.txid = txid
        self.signer = signer
        self.sig = sig
        self.status = status
        self.syntheticTxids = syntheticTxids 

class QueryResponse:
    def __init__(self, type, data, merkleState=None):
        self.type = type
        if merkleState:
            self.merkleState = MerkleState(**merkleState)

        if self.type == ACCUMULATE_TYPES.IDENTITY:
            self.identity = Identity(**data)
        elif self.type == ACCUMULATE_TYPES.LITE_TOKEN_ACCOUNT:
            self.liteTokenAccount = LiteTokenAccount(**data)
        elif self.type == ACCUMULATE_TYPES.KEY_PAGE:
            self.keyPage = KeyPage(**data)
        elif self.type == ACCUMULATE_TYPES.DATA_ENTRY:
            self.dataEntryQueryResponse = DataEntryQueryResponse(**data)
        elif self.type == ACCUMULATE_TYPES.KEY_PAGE_INDEX:
            self.keyPageIndex = ResponseKeyPageIndex(**data)
        elif self.type == ACCUMULATE_TYPES.METRICS:
            self.metricResponse = MetricsResponse(**data)
        
        
class QueryMultiResponse:
    def __init__(self, items, start, count, total):
        self.start = start
        self.count = count
        self.total = total
        self.items = list()
        for item in items:
            type = item.get('type') 
            if type== ACCUMULATE_TYPES.SYNTHETIC_DEPOSIT_TOKENS:
                self.items.append(SyntheticDepositTokens(**item))
            elif type == ACCUMULATE_TYPES.DIRECTORY:
                self.items.append(DirectoryQueryResult(**item))
            elif type == ACCUMULATE_TYPES.DATASET:
                self.items.append(DataEntryQueryResponse(**item))


class ResponseKeyPageIndex:
    def __init__(self, keyBook, keyPage, index=None):
        self.keyBook = keyBook
        self.keyPage = keyPage
        self.index = index

class TxResponse:
    def __init__(self, hash, message, txid, code = None, delivered=None):
        self.hash = hash
        self.message = message
        self.txid = txid
        self.code = code
        self.delivered = delivered