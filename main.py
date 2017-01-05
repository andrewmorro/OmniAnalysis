from analysis.TripleTop import TripleTop
import tushare as ts


stock_list = ts.get_today_all()['code']

tt = TripleTop()
#tt.analysis('603009')
for stock in stock_list:
    tt.analysis(stock)
