import sys


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
        data2 = data.loc[index - 1]
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
        data2 = data.loc[index - 1]
        if data1.close == round(data2.close * 1.1, 2) and data1.high != data1.low:
            return True
        else:
            return False

# 多个连续换手板(前N-1个板中至少有一个换手板）
class MultiTopClose(IRule):
    @classmethod
    def judge(cls, data, index, count):
        horizontal_flag = True
        for i in range(1, count+1):
            # There has to be as least one turnover top k prior to date index.
            if horizontal_flag and i < count + 1 and NotHorizontal.judge(data, index - i +1):
                horizontal_flag = False
            if not TopClose.judge(data, index - i +1):
                return False
        return not horizontal_flag


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

# 连续换手板
class TurnoverMulti(IRule):
    def __init__(self, n):
        self.n = n

    def judge(self, data, index):
        for i in range(self.n):
            if NotHorizontal.judge(data, index - i) is False:
                return False
        return True


# 实体两连板后，当日高开2-6%，收板
class TripleTopClose(IRule):
    @classmethod
    def judge(cls, data, index):
        data1 = data.loc[index]
        data2 = data.loc[index - 1]
        start = index - 2
        end = index + 1
        return NotHorizontalMulti(3).judge(data, index) and TopClose.judge(data, index) and TopClose.judge(data,
                                                                                                           index - 1) \
               and TopClose.judge(data,
                                  index - 2) and data1.open >= data2.close * 1.02 and data1.open <= data2.close * 1.06


# 实体两连板后，闷杀
class TripleTopCloseBad(IRule):
    @classmethod
    def judge(cls, data, index):
        data1 = data.loc[index]
        data2 = data.loc[index - 1]
        start = index - 3
        end = index + 1
        return NotHorizontalMulti(3).judge(data, index) and TopClose.judge(data, index - 1) \
               and TopClose.judge(data, index - 2) and data1.high < data2.close


class DoubleTopClose(IRule):
    @classmethod
    def judge(cls, data, index):
        return NotHorizontalMulti(2).judge(data, index) and TopClose.judge(data, index) \
               and TopClose.judge(data, index - 1)

# 冲板回落/炸板
class TopHatched(IRule):
    @classmethod
    def judge(cls, data, index):
        data1 = data.loc[index]
        data2 = data.loc[index-1]
        return data1.high == round(data2.close * 1.1, 2) and data1.high > data1.close and data1.high >= data1.open


# must use get_hist_data api
class HighTurnover(IRule):
    @classmethod
    def judge(cls, data, index):
        data1 = data.loc[index]
        return data1.turnover > 70


class Star(IRule):
    @classmethod
    def judge(cls, data, index):
        data1 = data.loc[index]
        return data1.high > data1.open and data1.high > data1.close and data1.low < data1.open and data1.low < data1.close \
               and abs(data1.close - data1.open) / data1.open < 0.03


class FuelUp(IRule):
    @classmethod
    def judge(cls, data, index):
        data1 = data.loc[index]
        data2 = data.loc[index - 1]

        return Star.judge(data, index) and TopClose.judge(data, index - 1) and data1.low > data2.high and data1.volume>data2.volume *2

# 测试规则1，板后跳空上下影中阳
class Rule1(IRule):
    @classmethod
    def judge(cls, data, index):
        data1 = data.loc[index]
        data2 = data.loc[index - 1]
        return TurnoverMulti(2).judge(data, index) and TopClose.judge(data, index - 1) \
               and data1.high > data1.close and data1.close> data1.open and data1.open> data1.low and data1.low>data2.high and data1.volume > data2.volume * 2

# 炸板
class TopFail(IRule):
    @classmethod
    def judge(cls, data, index):
        data1 = data.loc[index]
        data2 = data.loc[index - 1]
        return data1.high > data2.close * 1.1 -0.01 and data1.high > data1.close

# 2018-03-03 300353 similar


class Rule2(IRule):
    @classmethod
    def judge(cls, data, index):
        return TopFail.judge(data,index) and MultiTopClose.judge(data,index-1 , 3)


class RuleMatrix(IRule):

    def __init__(self, rule_list):
        self.rule_list = rule_list

    def judge(self, data, index):
        count = len(self.rule_list)
        for i in range(count):
            rule_class = getattr(sys.modules[__name__], self.rule_list[i])
            rule = rule_class()
            if not rule.judge(data, index - count + i + 1):
                return False
        return True


class Strategy(IRule):
    def __init__(self, ruleset=[]):
        self.ruleset = ruleset

    def addRule(self, rule: IRule):
        self.ruleset.append(rule)

    def judge(self, data, index):
        for rule in self.ruleset:
            if rule.judge(data, index) is False:
                return False
        return True
