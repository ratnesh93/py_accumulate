# py_accumulate

Python wrapper for accumulate API from https://accumulatenetwork.io/

This project is based on the theme Development Tools. In this project I have built a python sdk which would be serving as a wrapper for the accumulate methods.

Highlights of the python sdk:
- Methods based version 2 api  (https://testnet.accumulatenetwork.io/v2)
- Package contains github workflow which will publish library to pypi server, project can views at https://pypi.org/project/py-accumulate/
- Package contains test cases
- Package contains doc strings which shows the input of the methods
- All methods present in accumulate/internal/api/v2 methods.yml have been implemented


## install
'''python
pip install py_accumulate
'''

## pip

package link in pypi: https://pypi.org/project/py-accumulate/

## Usage

```python
from accumulate import Accumulate
ENDPOINT = "https://testnet.accumulatenetwork.io/v2"
a=Accumulate(ENDPOINT)
a.Version()
```

## Methods

|   METHOD_NAME     |       INPUT       |
| ------------- | ------------- |
|   Version()                   |   |
|   Metrics()                   |   metric, duration|
|Faucet()                       |  token_account_url|
|Query()                        |  token_account_url or ADI|
|QueryChain()                   |  CHAIN_ID|
|QueryTx()                      |  txId, wait|
|QueryTxHistory()               |  UrlQuery, QueryPagination|
|QueryData()                    |   Url, EntryHash|
|QueryKeyPageIndex()            |   Url, Key|
|QueryDataSet()                 |  Url, QueryPagination, QueryOptions|
|QueryDirectory()               |   UrlQuery, QueryPagination, QueryOptions|
|Execute()                      |   sponsor, signer, signature, keyPage, payload, checkOnly|
|ExecuteCreateAdi()             |   url, publicKey, keyBookName, keyPageName|
|ExecuteCreateDataAccount()     |   url, KeyBookUrl, ManagerKeyBookUrl|
|ExecuteCreateKeyBook()         |   url, Pages|
|ExecuteCreateKeyPage()         |   url, Keys|
|ExecuteCreateToken()           |   url, Symbol, Precision, Properties|
|ExecuteCreateTokenAccount()    |   url, TokenUrl, KeyBookUrl|
|ExecuteSendTokens()            |   To, Hash, Meta|
|ExecuteAddCredits()            |   Recipient, Amount|
|ExecuteUpdateKeyPage()         |   Operation, Key, NewKey, Owner|
|ExecuteWriteData()             |  DataEntry|


## Reference

-https://docs.accumulatenetwork.io/accumulate/developers/api/api-reference


## Developing testing

- Dependencies in requirements.txt
- Version Mangement in setup.cfg

```python
python -m unittest discover -s tests/accumulate/ -p 'test_*.py'
```