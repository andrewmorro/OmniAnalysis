import tushare as ts
from analysis.IAnalysis import IAnalysis
from analysis.Rule import *


class TripleTop(IAnalysis):

    def __init__(self):
        pass

    def analysis(self, stock_list):
        history = ts.get_k_data('000935')
        print(history[history.date == '2017-01-04'].low)

        for i in history.index:

            if i < 2:
                continue

            if NotHorizontal.judge(history.iloc[i]) and TopCloseRule.judge(history.iloc[i], history.iloc[i-1]) \
                    and TopCloseRule.judge(history.iloc[i-1], history.iloc[i-2]):
                print(history.iloc[i].date)
