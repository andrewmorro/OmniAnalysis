import tushare as ts
from analysis import IAnalysis


class TripleTop:

    def __init__(self):
        pass

    def analysis(self,stock_list):
        history = ts.get_k_data('000935',index='date')
        print(history.index)
        print(history.loc[1])
        '''
        for day in history['date']:
            print(day)
        '''