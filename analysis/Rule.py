class IRule(object):
    @classmethod
    def judge(cls):
        return None


class ISingleRule(IRule):
    @classmethod
    def judge(cls, data):
        return None


class IDoubleRule(IRule):
    @classmethod
    def judge(cls, data1, data2):
        return None


class ITripleRule(IRule):
    @classmethod
    def judge(cls, data1, data2, data3):
        return None


class TopCloseRule(IDoubleRule):
    @classmethod
    def judge(cls, data1, data2):
        if data1.close == round(data2.close * 1.1, 2):
            return True
        else:
            return False


class NotHorizontal(ISingleRule):
    @classmethod
    def judge(cls, data):
        if data.high != data.low:
            return True
        else:
            return False


class TripleTopClose(ITripleRule):
    @classmethod
    def judge(cls, data1, data2, data3, data4):
        return NotHorizontal.judge(data1) and NotHorizontal.judge(data2) and NotHorizontal.judge(data3) \
                and NotHorizontal.judge(data4) and TopCloseRule.judge(data1, data2) and TopCloseRule.judge(data2, data3) \
                and TopCloseRule.judge(data3, data4) and data1.open >= data2.close * 1.02 and data1.open <= data2.close * 1.05

