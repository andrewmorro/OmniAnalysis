class IRule(object):
    @classmethod
    def judge(cls, data, index):
        return None


# N天涨幅M
class Rise(IRule):
    @classmethod
    def judge(cls, data, index, n, pct):
        data1 = data.loc[index]
        data2 = data.loc[index - n - 1]
        if data1.high/data2.close >= 1+pct:
            return True
        else:
            return False

#涨停收盘
class TopClose(IRule):
    @classmethod
    def judge(cls, data, index):
        data1 = data.loc[index]
        data2 = data.loc[index-1]
        if data1.close == round(data2.close * 1.1, 2):
            return True
        else:
            return False

#非一字板
class NotHorizontal(IRule):
    @classmethod
    def judge(cls, data, index):
        if data.loc[index].high != data.loc[index].low:
            return True
        else:
            return False

#多日非一字板
class NotHorizontalMulti(IRule):
    @classmethod
    def judge(cls, data, index_list):
        result = True
        for index in index_list:
            result &= NotHorizontal.judge(data, index)
            if not result:
                break
        return result

#实体两连板后，当日高开2-5%，收板
class TripleTopClose(IRule):
    @classmethod
    def judge(cls, data, index):
        data1 = data.loc[index]
        data2 = data.loc[index-1]
        data3 = data.loc[index-2]
        data4 = data.loc[index-3]
        start = index-2
        end = index+1
        return NotHorizontalMulti.judge(data, range(start, end)) and TopClose.judge(data, index) and TopClose.judge(data, index - 1) \
               and TopClose.judge(data, index - 2) and data1.open >= data2.close * 1.02 and data1.open <= data2.close * 1.05

#实体两连板后，闷杀
class TripleTopCloseBad(IRule):
    @classmethod
    def judge(cls, data, index):
        data1 = data.loc[index]
        data2 = data.loc[index-1]
        data3 = data.loc[index-2]
        data4 = data.loc[index-3]
        start = index-3
        end = index+1
        return NotHorizontalMulti.judge(data, range(start, end)) and TopClose.judge(data, index - 1) \
               and TopClose.judge(data, index - 2) and data1.high < data2.close