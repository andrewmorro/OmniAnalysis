import tushare as ts
import pandas as pd
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
        cols = ['Code', 'Date', 'open_profit', 'low_profit', 'high_profit', 'close_profit']
        df = DataFrame(columns=cols)
        pro = ts.pro_api()

        for stock in stock_list:
            try:

                print('Analyze : ' + stock)
                history = pro.daily(ts_code=stock, start_date=start, end_date=end).sort_values(by=['trade_date'])
                for i in range(0, len(history)):
                    try:
                        if rule.judge(history, i):
                            profit = self.analyzeProfitEffect(history, i)
                            df.loc[len(df)] = [stock, history.iloc[i].trade_date] + profit
                    except Exception as e:
                        print(e)
                        continue
            except Exception as e:
                print(e)
                continue
        return df

    def analyzeProfitEffect(self, data, index):
        if index >= len(data) - 1:
            return [None, None, None]
        today = data.iloc[index]
        nextday = data.iloc[index + 1]
        open_profit = (nextday.open - today.high) / today.high * 100
        low_profit = (nextday.low - today.high) / today.high * 100
        high_profit = (nextday.high - today.high) / today.high * 100
        close_profit = (nextday.close - today.high) / today.high * 100
        return [round(open_profit, 2), round(low_profit, 2), round(high_profit, 2), round(close_profit, 2)]
