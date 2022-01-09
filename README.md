# py_accumulate

Python wrapper for accumulate API

## Usage

```python
from py_accumulate.py_accumulate import Accumulate
ENDPOINT = "https://testnet.accumulatenetwork.io/v1"
a=Accumulate(ENDPOINT)
url = "acc://d4c8d9ab07daeecf50a7c78ff03c6524d941299e5601e578/ACME"
a.get(url)
```

## Endpoints

- get 


## Reference

-https://docs.accumulatenetwork.io/accumulate/developers/api/api-reference