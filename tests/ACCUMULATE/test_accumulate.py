import unittest
import sys
import os
sys.path.append(os.path.abspath('..'))
sys.path.append(os.path.abspath('../src'))
from ACCUMULATE import Accumulate


class TestClassAccumulate(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        self.endpoint = "https://testnet.accumulatenetwork.io/v2"
        self.accumulate = Accumulate(self.endpoint)
        super().__init__(methodName=methodName)

    def test_version(self):
        res = self.accumulate.Version()
        self.assertIsNotNone(res)
        self.assertIsNotNone(res.type)
        self.assertEqual(res.type,'version')
        self.assertIsNotNone(res.version)
        self.assertIsNotNone(res.version.commit)
        self.assertIsNotNone(res.version.version)
        self.assertIsNotNone(res.version.versionIsknown)
        self.assertEqual(res.version.versionIsknown, True)
        
    # def test_get(self):
    #     url = "acc://d4c8d9ab07daeecf50a7c78ff03c6524d941299e5601e578/ACME"
    #     res = self.accumulate.get(url)
    #     self.assertIsNotNone(res)
    #     self.assertIsNotNone(res.get('data',None))
    #     self.assertEqual(res.get('data',dict()).get('url'),url)
    
    # def test_query(self):
    #     url = "acc://d4c8d9ab07daeecf50a7c78ff03c6524d941299e5601e578/ACME"
    #     res = self.accumulate.get(url)
    #     self.assertIsNotNone(res)
    #     self.assertIsNotNone(res.get('data',None))
    #     print(res)