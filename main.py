from analysis.TripleTop import TripleTop
import tushare as ts

test = False
#test = True
tt = TripleTop()
if test:
    tt.analysis('000935')
else:
    stock_list = ts.get_today_all()['code']
    for stock in stock_list:
        tt.analysis(stock)
