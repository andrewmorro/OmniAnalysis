from analysis.stockfilters.AbstractStockFilter import AbstractStockFilter
from analysis.marketdata.MarketDataService import MarketDataService


class RepairedTopFilter(AbstractStockFilter):

    def __init__(self):
        pass

    def filter(self, stockList, startdate, enddate):
        return super(RepairedTopFilter, self).filter(stockList, startdate, enddate)

    def doJudge(self, stock, date):
        #print("RepairedTopFilter doJudge - {} {}".format(stock,date))
        ds = MarketDataService();
        tickData = ds.getTickData(stock,date)
        firstTopTime = None
        repairedTime = None
        firstHitTop = None
        brokenTop = None
        repairedTop = False
        topPrice = ds.getTopPrice(stock, date)


        for index, row in tickData.iterrows():
            if(row['price'] == topPrice):
                if firstHitTop is None:
                    """ First time the price hits top."""
                    firstHitTop = True
                    firstTopTime = row['time']
                if brokenTop is True:
                    """ Broken, repairing top i.e. hit top for at least 1 time."""
                    repairedTop = True
                    repairedTime = row['time']
            else:
                """ price is not top, not repairing top or didn't hit top at all"""
                repairedTime = None
                repairedTop = False
                if firstHitTop == True:
                    brokenTop = True

        return repairedTop
