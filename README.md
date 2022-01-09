# py_accumulate

Python wrapper for accumulate API


## install
'''python
pip install py_accumulate
'''
## Usage

```python
from py_accumulate import Accumulate
ENDPOINT = "https://testnet.accumulatenetwork.io/v1"
a=Accumulate(ENDPOINT)
url = "acc://d4c8d9ab07daeecf50a7c78ff03c6524d941299e5601e578/ACME"
a.get(url)
```

## Endpoints

- get 


## Reference

-https://docs.accumulatenetwork.io/accumulate/developers/api/api-reference


## pip

https://pypi.org/project/py-accumulate/0.0.1/#description

## Developing testing

```python
python -m unittest discover -s tests/py_accumulate/ -p 'test_*.py'
```