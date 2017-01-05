import tushare as ts
from analysis.IAnalysis import IAnalysis
from analysis.Rule import *


class TripleTop(IAnalysis):

    def __init__(self):
        pass

    def analysis(self, stock):
        history = ts.get_k_data(stock, start='2016-07-01', end='2017-01-05')
        #print(history)
        has_result = False
        for i in history.index[3:]:
#            if NotHorizontal.judge(history.iloc[i]) and TopCloseRule.judge(history.iloc[i], history.iloc[i-1]) \
#                    and TopCloseRule.judge(history.iloc[i-1], history.iloc[i-2]):
#            if TripleTopClose.judge(history.loc[i], history.loc[i-1], history.loc[i-2], history.loc[i-3]):
            if TripleTopCloseBad.judge(history.loc[i], history.loc[i-1], history.loc[i-2], history.loc[i-3]):
                # Make sure prints title line to console only if necessary.
                if not has_result:
                    print("TripleTop date for {}:".format(stock))
                    has_result = True
                print(history.loc[i].date)
