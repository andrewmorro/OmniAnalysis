class IRule(object):
    @classmethod
    def judge(cls, data, index):
        return None


# N天涨幅M
class Rise(IRule):
    def __init__(self, n, pct):
        self.n = n
        self.pct = pct

    def judge(self, data, index):
        data1 = data.loc[index]
        data2 = data.loc[index - self.n]
        if data1.high / data2.close >= 1 + self.pct:
            return True
        else:
            return False


class VolUp(IRule):
    @classmethod
    def judge(cls, data, index):
        data1 = data.loc[index]
        data2 = data.loc[index-1]
        if data1.volume >= data2.volume:
            return True
        else:
            return False


class VolDown(IRule):
    @classmethod
    def judge(cls, data, index):
        data1 = data.loc[index]
        data2 = data.loc[index - 1]
        if data1.volume < data2.volume:
            return True
        else:
            return False


class VolExplode(IRule):
    def __init__(self, n):
        self.n = n

    def judge(self, data, index):
        data1 = data.loc[index]
        data2 = data.loc[index - 1]
        if data1.volume >= data2.volume * self.n:
            return True
        else:
            return False


# 涨停收盘
class TopClose(IRule):
    @classmethod
    def judge(cls, data, index):
        data1 = data.loc[index]
        data2 = data.loc[index-1]
        if data1.close == round(data2.close * 1.1, 2):
            return True
        else:
            return False


# 非一字板
class NotHorizontal(IRule):
    @classmethod
    def judge(cls, data, index):
        if data.loc[index].high != data.loc[index].low:
            return True
        else:
            return False


# 多日非一字板
class NotHorizontalMulti(IRule):
    def __init__(self, n):
        self.n = n

    def judge(self, data, index):
        for i in range(self.n):
            if NotHorizontal.judge(data, index - i) is True:
                return True
        return False



# 实体两连板后，当日高开2-6%，收板
class TripleTopClose(IRule):
    @classmethod
    def judge(cls, data, index):
        data1 = data.loc[index]
        data2 = data.loc[index-1]
        start = index-2
        end = index+1
        return NotHorizontalMulti(3).judge(data, index) and TopClose.judge(data, index) and TopClose.judge(data, index - 1) \
               and TopClose.judge(data, index - 2) and data1.open >= data2.close * 1.02 and data1.open <= data2.close * 1.06


# 实体两连板后，闷杀
class TripleTopCloseBad(IRule):
    @classmethod
    def judge(cls, data, index):
        data1 = data.loc[index]
        data2 = data.loc[index-1]
        start = index-3
        end = index+1
        return NotHorizontalMulti(3).judge(data, index) and TopClose.judge(data, index - 1) \
               and TopClose.judge(data, index - 2) and data1.high < data2.close


class DoubleTopClose(IRule):
    @classmethod
    def judge(cls, data, index):
        return NotHorizontalMulti(2).judge(data, index) and TopClose.judge(data, index) \
               and TopClose.judge(data, index - 1)

class TopHatched(IRule):
    @classmethod
    def judge(cls, data, index):
        data1 = data.loc[index]
        data2 = data.loc[index-1]
        return data1.high == round(data2.close * 1.1, 2) and data1.high > data1.close and data1.high > data1.open

# must use get_hist_data api
class HighTurnover(IRule):
    @classmethod
    def judge(cls, data, index):
        data1 = data.loc[index]
        return data1.turnover > 60


class Strategy(IRule):
    def __init__(self, ruleset = []):
        self.ruleset = ruleset

    def addRule(self, rule:IRule):
        self.ruleset.append(rule)

    def judge(self, data, index):
        for rule in self.ruleset:
            if rule.judge(data, index) is False:
                return False
        return True