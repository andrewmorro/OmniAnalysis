import tushare as ts
import sys
from analysis.IAnalysis import IAnalysis
from analysis.Rule import *


class GeneralAnalysis(IAnalysis):

    def __init__(self):
        pass

    def analysis(self, stock_list=['603777'], rule_name='TripleTopClose',start='2016-07-01', end='2017-01-05'):
        for stock in stock_list:
            history = ts.get_k_data(stock, start, end)
            has_result = False
            rule_class = getattr(sys.modules['analysis.Rule'], rule_name)
            for i in history.index[3:]:
                if rule_class.judge(history, i):
                    # Make sure prints title line to console only if necessary.
                    if not has_result:
                        print("TripleTop date for {}:".format(stock))
                        has_result = True
                    print(history.loc[i].date)
