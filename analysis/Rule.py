class IRule(object):
    @classmethod
    def judge(cls, data, index):
        return None

#涨停收盘
class TopCloseRule(IRule):
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

#实体三连板，当日高开2-5%
class TripleTopClose(IRule):
    @classmethod
    def judge(cls, data, index):
        data1 = data.loc[index]
        data2 = data.loc[index-1]
        data3 = data.loc[index-2]
        data4 = data.loc[index-3]
        start = index-2
        end = index+1
        return NotHorizontalMulti.judge(data, range(start, end)) and TopCloseRule.judge(data,index) and TopCloseRule.judge(data,index-1) \
                and TopCloseRule.judge(data,index-2) and data1.open >= data2.close * 1.02 and data1.open <= data2.close * 1.05


class TripleTopCloseBad(IRule):
    @classmethod
    def judge(cls, data, index):
        data1 = data.loc[index]
        data2 = data.loc[index-1]
        data3 = data.loc[index-2]
        data4 = data.loc[index-3]
        start = index-3
        end = index+1
        return NotHorizontalMulti.judge(data, range(start, end)) and TopCloseRule.judge(data,index) and TopCloseRule.judge(data,index-1) \
                and TopCloseRule.judge(data,index-2) and data1.open >= data2.close * 1.02 and data1.open <= data2.close * 1.05 and data1.close<data2.close