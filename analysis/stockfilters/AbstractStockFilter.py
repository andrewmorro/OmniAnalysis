from abc import ABCMeta, abstractmethod
from datetime import timedelta, date, datetime
from pandas import DataFrame
from analysis.marketdata.MarketDataService import MarketDataService
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading


class AbstractStockFilter(metaclass=ABCMeta):
    """Interface of the stock filters"""

    def filter(self, stockList, startdate, enddate):
        """ Analyze the stocks in the stockList within the data range and filter by the rules defined in the concrete class"""

        executor = ThreadPoolExecutor(max_workers=10)
        df = DataFrame(columns=['Code', 'Date'])
        with executor:
            mds = MarketDataService()

            futures = []
            args = []
            for stock in stockList:
                for dateStr in mds.tradedatestr(startdate, enddate):
                    args.append((stock, dateStr))

            for result in executor.map(lambda p: self.judge(*p), args):
                if result[2]:
                    df.loc[len(df)] = [result[0], result[1]]

        return df

    def judge(self, stock, date):
        """ General judge method that calls abstract doJudge concrete method. Append parameters(stock, date) to facilitate result manipulation for thread Future. """
        try:
            return stock, date, self.doJudge(stock, date)
        except Exception:
            return stock, date, False

    @abstractmethod
    def doJudge(self, stock, date):
        """ Judge if the stock on the specific date satisfied the filter/rule"""
        """ Returns a boolean"""
        pass
