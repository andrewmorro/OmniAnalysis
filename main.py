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

stock = '000856'
date = '2017-04-25'
day = ts.get_hist_data(code=stock, start=date,end=date)
pre_close = day['close'].values[0]-day['price_change'].values[0]



df = ts.get_tick_data(stock, date=date)
df = df.sort_values(by='time')
time = datetime.time(9, 25)

# change to use sub string to match time - should achieve speed optimization
print(datetime.datetime.now())
for index, row in df.iterrows():
    temp_time = datetime.datetime.strptime(row['time'], '%H:%M:%S').time()
    if temp_time >= time:
        print(row['price'])
        if time == datetime.time(9, 25):
            time = datetime.time(9, 30)
        elif time == datetime.time(11, 30):
            time = datetime.time(13, 00)
        else:
            time = (datetime.datetime.combine(datetime.date.today(),time) + datetime.timedelta(minutes=1)).time()


print(datetime.datetime.now())

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