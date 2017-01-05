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


class TopCloseRule(IDoubleRule):
    @classmethod
    def judge(cls, data1, data2):
        if data1.close == round(data2.close*1.1, 2):
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

