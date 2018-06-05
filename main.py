from analysis.GeneralAnalysis import GeneralAnalysis
from analysis import RuleConfig
from analysis import Rule
from analysis import ClusterAnalysis
import tushare as ts
import pandas
import os


base_path = 'F:\\BaiduSync\\trade\\总结\\量化\\cache\\'
if os.environ["ENV"] == "COMPANY":
    base_path = 'D:\\百度云同步盘\\trade\\总结\\量化\\cache\\'
elif os.environ['ENV'] == "MAC":
    base_path = '/Users/andrew/百度云同步盘/trade/总结/量化/'

print(base_path)


test = False
#test = True

tt = GeneralAnalysis()
stock_list = []

# token for cache access
token = 'RuleNStyle-20180605.xlsx'
sample_token = 'sample_cache_7852.xlsx'

df = None
sample = None
try:
    df = pandas.read_excel(base_path+token,converters={'Code':str})
    sample = pandas.read_excel(base_path+sample_token)
except Exception:
    print('Dataframe cache not found.')





# stock = '000856'
# date = '2017-04-27'
# data = get_1M(stock, date)
#
# print(len(data))

if df is None:
    if test:
        stock_list = ['300353']

    else:

        stock_list = ts.get_today_all()['code']
        # print(len(stock_list))

    # analyze by rule name
    rule_name = 'NStyle'
    df = tt.analysisByRuleName(rule_name,stock_list,start='2018-05-01')

    # analyze by rule
    #rule_list = ['TopClose','TopClose','TopClose']
    #rule = Rule.RuleMatrix(rule_list)
    #df = tt.analysisByRule(rule,stock_list,start='2016-02-26')

    df.to_excel(base_path+token)
else:
    print("Using cache for rule analysis...")


#sample = ClusterAnalysis.prepare_sample(base_path+sample_token, df)
#pred = ClusterAnalysis.show_clustered(sample, 3)

#print(pred[2])

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