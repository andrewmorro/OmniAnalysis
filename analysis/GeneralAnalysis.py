import tushare as ts
import sys
from pandas import DataFrame
from analysis.IAnalysis import IAnalysis
import datetime
from analysis.Rule import *


class GeneralAnalysis(IAnalysis):

    def __init__(self):
        pass

    def analysisByRuleName(self,  rule_name='TripleTopClose', stock_list=['603777'], start=None, end=None):
        rule_class = getattr(sys.modules['analysis.Rule'], rule_name)
        rule = rule_class()
        return self.analysisByRule(rule, stock_list, start, end)

    def analysisByRule(self, rule, stock_list=['603777'] , start='2016-07-01', end=None):
        if end is None:
            end = datetime.datetime.now().strftime('%Y-%m-%d')
        if start is None:
            start = (datetime.datetime.now()-datetime.timedelta(days=7)).strftime('%Y-%m-%d')
        df = DataFrame(columns=['Code', 'Date'])
        for stock in stock_list:
            history = ts.get_k_data(stock, start, end)
            for i in history.index[3:]:
                if rule.judge(history, i):
                    df.loc[len(df)] = [stock, history.loc[i].date]
        return df