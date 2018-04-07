
import tushare as ts
import numpy
from datetime import timedelta, date,datetime

class MarketDataService:

    def tradedatestr(self,startdate, enddate):

        start = datetime.strptime(startdate, "%Y-%m-%d")
        end = datetime.strptime(enddate, "%Y-%m-%d")
        for n in range(int((end - start).days)):
            the_date = start + timedelta(n)
            dateStr = the_date.strftime("%Y-%m-%d")
            # is_holiday api is way too slow.
            #if ts.is_holiday(dateStr):
            if the_date.date().weekday() >= 5:
                continue
            yield dateStr

    def getAllTickers(self):
        return ts.get_today_all()['code']

    def getDayHistData(self,stock,start,end):
        day = ts.get_hist_data(code=stock, start=date, end=date)
        if day is None:
            raise Exception("Error - None returned by getDayHistData {} {} {}".format(stock,start,end))
        return day


    def getPreClose(self, stock, date):
        day = ts.get_hist_data(code=stock, start=date, end=date)
        pre_close = day['close'].values[0] - day['price_change'].values[0]
        return pre_close

    def getTopPrice(self, stock, date):
        pre_close = self.getPreClose(stock, date)
        top = round(pre_close * 1.1, 2)
        return top

    def getTickData(self, stock, date):
        try:
            # src : 数据源选择，可输入sn(新浪)、tt(腾讯)、nt(网易)，默认sn
            df = ts.get_tick_data(stock, date=date, pause=0.1, src='tt')
            df = df.sort_values(by='time')
            return df
        except Exception as err:
            print('Error - getTickData {} {} {}'.format(stock, date, err))
            return None

    def next_1M(self, the_time):
        if the_time.time() == datetime.time(9, 25):
            the_time = the_time + datetime.timedelta(minutes=5)
        elif the_time.time() == datetime.time(11, 30):
            the_time = the_time + datetime.timedelta(minutes=90)
        else:
            the_time = the_time + datetime.timedelta(minutes=1)
        return the_time

    def get_1M(self, stock, date):
        pre_close = self.getPreClose(stock,date)
        df = self.getTickData(stock, date)
        result = []

        # TODO:change to use sub string to match time - should achieve speed optimization
        index_time = datetime.datetime.combine(datetime.date.today(), datetime.time(9, 25))
        pct = 0;
        for index, row in df.iterrows():
            temp_time = datetime.datetime.combine(datetime.date.today(),
                                                  datetime.datetime.strptime(row['time'], '%H:%M:%S').time())
            delta = temp_time - index_time
            if delta.days < 0:
                # current row falls behind index, skip.
                continue

            while delta.seconds >= 60 and delta.days >= 0:
                # fill missing values
                result.append(pct)
                # update time to next index
                index_time = self.next_1M(index_time)
                delta = temp_time - index_time

            if delta.seconds >= 0 and delta.seconds < 60:
                pct = numpy.round((row['price'] - pre_close) / pre_close * 100, 2)
                # print('{} - {}'.format(row['time'],pct))
                result.append(pct)
                # update time to next index
                index_time = self.next_1M(index_time)

        if len(result) < 240:
            print('{} {} sample collected - {}'.format(stock, date, len(result)))
        while len(result) < 243:
            result.append(10.00)
        return result
