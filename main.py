from analysis.GeneralAnalysis import GeneralAnalysis
from analysis import RuleConfig
from analysis import Rule
import tushare as ts
import datetime
import numpy
import pandas


from sklearn.cluster import KMeans

import matplotlib.pyplot as plt


test = False
#test = True

base_path = 'F:\\BaiduSync\\trade\\总结\\量化\\cache\\'
tt = GeneralAnalysis()
stock_list = []

# token for cache access
token = 'doubletop2342342.xlsx'
sample_token = 'sample_cache_23423908.xlsx'

df = None
sample = None
try:
    df = pandas.read_excel(base_path+token,converters={'Code':str})
    sample = pandas.read_excel(base_path+sample_token)
except Exception:
    print('No cache found.')



def next_1M(the_time):
    if the_time.time() == datetime.time(9, 25):
        the_time = the_time + datetime.timedelta(minutes=5)
    elif the_time.time() == datetime.time(11, 30):
        the_time = the_time + datetime.timedelta(minutes=90)
    else:
        the_time = the_time + datetime.timedelta(minutes=1)
    return the_time



def get_1M(stock, date):
    df = None
    try:
        day = ts.get_hist_data(code=stock, start=date,end=date)
        pre_close = day['close'].values[0]-day['price_change'].values[0]

        #src : 数据源选择，可输入sn(新浪)、tt(腾讯)、nt(网易)，默认sn
        df = ts.get_tick_data(stock, date=date,pause=0.1,src='tt')
        df = df.sort_values(by='time')
        print('{} {} tick data retrived.'.format(stock, date))
    except Exception:
        print('Error - Failed to retrive tick data.')
        return None
    result = []

    # TODO:change to use sub string to match time - should achieve speed optimization
    index_time = datetime.datetime.combine(datetime.date.today(),datetime.time(9, 25))
    pct = 0;
    for index, row in df.iterrows():
        temp_time = datetime.datetime.combine(datetime.date.today(),datetime.datetime.strptime(row['time'],'%H:%M:%S').time())
        delta = temp_time - index_time
        if delta.days<0:
            #current row falls behind index, skip.
            continue

        while delta.seconds >= 60 and delta.days >= 0:
            # fill missing values
            result.append(pct)
            # update time to next index
            index_time = next_1M(index_time)
            delta = temp_time - index_time

        if delta.seconds>=0 and delta.seconds<60:
            pct = numpy.round((row['price'] - pre_close) / pre_close * 100, 2)
            #print('{} - {}'.format(row['time'],pct))
            result.append(pct)
            # update time to next index
            index_time = next_1M(index_time)

    if len(result) < 240:
        print('{} {} sample collected - {}'.format(stock, date, len(result)))
    while len(result) < 243:
        result.append(10.00)
    return result


# stock = '000856'
# date = '2017-04-27'
# data = get_1M(stock, date)
#
# print(len(data))

if df is None:
    if test:
        stock_list = ['000856']

    else:

        stock_list = ts.get_today_all()['code']
        # print(len(stock_list))
    rule_name = 'DoubleTopClose'

    df = tt.analysisByRuleName(rule_name,stock_list,start='2016-06-01')
    df.to_excel(base_path+token)
else:
    print("Using cache for rule analysis...")

if sample is None:
    result = []
    book = []
    for index, row in df.iterrows():
        data = get_1M(row['Code'], row['Date'])
        if data is not None and len(data) == 243:
            book.append((row['Code'], row['Date']))
            result.append(data)

    print("Start clustering...")
    if len(result)<=0:
        print('No Samples.')
        exit(0)
    sample = pandas.DataFrame(result)

    sample.to_excel(base_path+sample_token)
else:
    print("Using cache for samples...")


kmeans = KMeans(n_clusters=10)
pred = kmeans.fit_predict(sample,y=[len(sample),243])
print(kmeans.cluster_centers_)
#plt.figure(figsize=(12, 12))
for center in kmeans.cluster_centers_:
    plt.plot(center)
plt.show()


print(pred)

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