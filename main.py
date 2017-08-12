from analysis.GeneralAnalysis import GeneralAnalysis
from analysis import RuleConfig
from analysis import Rule
import tushare as ts
import datetime

#test = False
test = True


tt = GeneralAnalysis()
stock_list = []
if test:
    stock_list = ['000856']

else:
    stock_list = ts.get_today_all()['code']
    # print(len(stock_list))


print(data)
# rule_name = 'DoubleTopClose'
#
# df = tt.analysisByRuleName(rule_name,stock_list,start='2017-04-01')
#
# for index, row in df.iterrows():
#     data = ts.get_k_data(code=row['Code'],start=row['Date'],end=row['Date'], ktype='5')
#     print(data)
    #prices = data.loc[:,"close"]
    #print(prices)


# df.to_excel(r'F:\BaiduSync\trade\总结\量化\{}-{}.xlsx'.format(RuleConfig.rule[rule_name],datetime.datetime.now().strftime('%Y-%m-%d-%H-%M')), sheet_name=RuleConfig.rule[rule_name])


#
# rise = Rule.Rise(5,0.4)
# notHori = Rule.NotHorizontalMulti(2)
# strategy = Rule.Strategy()
# strategy.addRule(rise)
# strategy.addRule(notHori)

#   df = tt.analysisByRule(strategy,stock_list,start='2014-06-01',period=5)
#    df.to_excel(r'F:\BaiduSync\trade\总结\量化\{}-{}.xlsx'.format('五天四板',datetime.datetime.now().strftime('%Y-%m-%d-%H-%M')), sheet_name='五天四板')


#print(df)