import unittest
from analysis.stockfilters.RepairedTopFilter import RepairedTopFilter
from analysis.marketdata.MarketDataService import MarketDataService
from export.ExcelExporter import ExcelExporter


class StockFiltersTest(unittest.TestCase):

    @unittest.skip("reason for skipping")
    def testFilter(self):
        filter = RepairedTopFilter()
        self.assertEqual(False, filter.judge("601186", "2018-04-03"))
        self.assertEqual(True, filter.judge("300624", "2018-04-04"))
        self.assertEqual(False, filter.judge("300624", "2018-03-01"))
        self.assertEqual(True, filter.judge("300624", "2018-03-02"))
        self.assertEqual(True, filter.judge("300624", "2018-03-05"))
        self.assertEqual(True, filter.judge("300624", "2018-03-06"))
        self.assertEqual(False, filter.judge("002864", "2018-03-21"))
        self.assertEqual(False, filter.judge("300598", "2018-03-27"))

    def testFindRepairedTop(self):
        mds = MarketDataService()
        filter = RepairedTopFilter()
        df = filter.filter(mds.getAllTickers(), '2018-03-01', '2018-04-01')
        # df = filter.filter(['300624', '002846', '300676'], '2018-03-01', '2018-04-01')
        df.to_excel('F:\\BaiduSync\\trade\\总结\\量化\\cache\\20180407.xlsx', '烂板')
        #print(df)


if __name__ == '__main__':
    unittest.main()
