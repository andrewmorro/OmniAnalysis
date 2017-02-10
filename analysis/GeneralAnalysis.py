import tushare as ts
import sys
from pandas import DataFrame
from analysis.IAnalysis import IAnalysis
from analysis.Rule import *


class GeneralAnalysis(IAnalysis):

    def __init__(self):
        pass

    def analysis(self, stock_list=['603777'], rule_name='TripleTopClose',start='2016-07-01', end='2017-01-05'):
        df = DataFrame(columns=['Code', 'Date'])
        for stock in stock_list:
            history = ts.get_k_data(stock, start, end)
            rule_class = getattr(sys.modules['analysis.Rule'], rule_name)
            for i in history.index[3:]:
                if rule_class.judge(history, i):
                    df.loc[len(df)] = [stock, history.loc[i].date]
        return df
