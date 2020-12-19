import tushare as ts
import sys
from pandas import DataFrame
from analysis.IAnalysis import IAnalysis
import datetime
from analysis.Rule import *


class GeneralAnalysis(IAnalysis):

    def __init__(self):
        pass

    # hist is a switch that tells the code to use get_hist_data api to fetch some special data such as turnover.
    def analysisByRuleName(self, rule_name='TripleTopClose', stock_list=['603777'], start=None, end=None, period=2):
        rule_class = getattr(sys.modules['analysis.Rule'], rule_name)
        rule = rule_class()
        return self.analysisByRule(rule, stock_list, start, end, period)

    def analysisByRule(self, rule, stock_list=['603777.SH'], start='20160701', end=None, period=1):
        if end is None:
            end = datetime.datetime.now().strftime('%Y%m%d')
        if start is None:
            start = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime('%Y%m%d')
        df = DataFrame(columns=['Code', 'Date'])
        pro = ts.pro_api()

        for stock in stock_list:
            try:

                print('Analyze : ' + stock)
                history = pro.daily(ts_code=stock, start_date=start, end_date=end)
                for i in history.index[period:]:
                    try:
                        if rule.judge(history, i):
                            df.loc[len(df)] = [stock, history.loc[i].trade_date]
                    except Exception as e:
                        print(e)
                        continue
            except Exception:
                continue
        return df
