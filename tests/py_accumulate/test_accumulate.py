import unittest
import sys
import os
sys.path.append(os.path.abspath('..'))
sys.path.append(os.path.abspath('../src'))
from src.py_accumulate import Accumulate


class TestClassAccumulate(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        self.endpoint = "https://testnet.accumulatenetwork.io/v1"
        self.accumulate = Accumulate(self.endpoint)
        super().__init__(methodName=methodName)

    def test_version(self):
        res = self.accumulate.version()
        self.assertIsNotNone(res)
        self.assertIsNotNone(res.get('type',None))
        self.assertEqual(res.get('type'),'version')
        
    def test_get(self):
        url = "acc://d4c8d9ab07daeecf50a7c78ff03c6524d941299e5601e578/ACME"
        res = self.accumulate.get(url)
        self.assertIsNotNone(res)
        self.assertIsNotNone(res.get('data',None))
        self.assertEqual(res.get('data',dict()).get('url'),url)