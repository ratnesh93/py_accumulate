import unittest
import sys
import os

sys.path.append(os.path.abspath(".."))
sys.path.append(os.path.abspath("../ACCUMULATE"))
from ACCUMULATE import Accumulate
from ACCUMULATE.constants import ACCUMULATE_TYPES


class TestClassAccumulate(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        self.endpoint = "https://testnet.accumulatenetwork.io/v2"
        self.URL_acc = "acc://d4c8d9ab07daeecf50a7c78ff03c6524d941299e5601e578/ACME"
        self.ADI = "adione"
        self.chainId = (
            "12e2d2d82f7b65752b3fd8d37d195f6d87f6cb24b83c4ae70f4571ea1007e741"
        )
        self.txId = "9dce91ec75f5b5e767283d8db77394daeef6e50b4f0e1197624f1a888ed076b1"
        self.URL_queryData = "acc://aditwo/aditwodata"
        self.entryHash = (
            "b45fa53718dbc5bf31f2f6134d1ff84fe22b3760face9c2ab012fd66d16d1808"
        )

        self.accumulate = Accumulate(self.endpoint)
        super().__init__(methodName=methodName)

    def test_version(self):
        res = self.accumulate.Version()
        self.assertIsNotNone(res)
        self.assertIsNotNone(res.type)
        self.assertEqual(res.type, ACCUMULATE_TYPES.VERSION)
        self.assertIsNotNone(res.version)
        self.assertIsNotNone(res.version.commit)
        self.assertIsNotNone(res.version.version)
        self.assertIsNotNone(res.version.versionIsknown)
        self.assertEqual(res.version.versionIsknown, True)

    def test_metrics(self):
        metric = "tps"
        duration = "1h"
        res = self.accumulate.Metrics(metric, duration)
        self.assertIsNotNone(res)
        self.assertIsNotNone(res.type)
        self.assertEqual(res.type, ACCUMULATE_TYPES.METRICS)
        self.assertIsNotNone(res.metricResponse)
        self.assertIsNotNone(res.metricResponse.value)

    def test_faucet(self):
        res = self.accumulate.Faucet(self.URL_acc)
        self.assertIsNotNone(res)
        self.assertIsNotNone(res.txid)

    def test_query_accURL(self):
        res = self.accumulate.Query(self.URL_acc)
        self.assertIsNotNone(res)
        self.assertIsNotNone(res.type)
        self.assertIsNotNone(res.merkleState)
        self.assertIsNotNone(res.liteTokenAccount)

    def test_query_ADI(self):
        res = self.accumulate.Query(self.ADI)
        self.assertIsNotNone(res)
        self.assertIsNotNone(res.type)
        self.assertIsNotNone(res.merkleState)
        self.assertIsNotNone(res.identity)

    def test_queryChain(self):
        res = self.accumulate.QueryChain(self.chainId)
        self.assertIsNotNone(res)
        self.assertIsNotNone(res.type)
        self.assertIsNotNone(res.merkleState)
        self.assertIsNotNone(res.keyPage)

    def test_queryTx(self):
        # args only txid
        res = self.accumulate.QueryTx(self.txId)
        self.assertIsNotNone(res)
        self.assertIsNotNone(res.type)
        self.assertEqual(res.type, ACCUMULATE_TYPES.ACME_FAUCET)
        # args both txid and wait
        res = self.accumulate.QueryTx(self.txId, 2)
        self.assertIsNotNone(res)
        self.assertIsNotNone(res.type)
        self.assertEqual(res.type, ACCUMULATE_TYPES.ACME_FAUCET)

    def test_queryTxHistory(self):
        # args: url, count
        res = self.accumulate.QueryTxHistory(self.URL_acc, 2)
        self.assertIsNotNone(res)
        self.assertIsNotNone(res.items)
        self.assertIsNotNone(res.start)
        self.assertIsNotNone(res.count)
        self.assertIsNotNone(res.total)
        # args: url, count, start
        res = self.accumulate.QueryTxHistory(self.URL_acc, 2, 1)
        self.assertIsNotNone(res)
        self.assertIsNotNone(res.items)
        self.assertIsNotNone(res.start)
        self.assertIsNotNone(res.count)
        self.assertIsNotNone(res.total)

    def test_queryData(self):
        # args: URL_queryData
        res = self.accumulate.QueryData(self.URL_queryData)
        self.assertIsNotNone(res)
        self.assertIsNotNone(res.type)
        self.assertIsNotNone(res.merkleState)
        self.assertIsNotNone(res.dataEntryQueryResponse)
        self.assertIsNotNone(res.dataEntryQueryResponse.entry)
        self.assertIsNotNone(res.dataEntryQueryResponse.entry.data)
        self.assertIsNotNone(res.dataEntryQueryResponse.entryHash)
        # args: URL_queryData, entryHash
        res = self.accumulate.QueryData(self.URL_queryData, self.entryHash)
        self.assertIsNotNone(res)
        self.assertIsNotNone(res.type)
        self.assertIsNotNone(res.merkleState)
        self.assertIsNotNone(res.dataEntryQueryResponse)
        self.assertIsNotNone(res.dataEntryQueryResponse.entry)
        self.assertIsNotNone(res.dataEntryQueryResponse.entry.data)
        self.assertIsNotNone(res.dataEntryQueryResponse.entryHash)
