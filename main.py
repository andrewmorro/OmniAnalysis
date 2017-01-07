from analysis.GeneralAnalysis import GeneralAnalysis
from analysis import RuleConfig
import tushare as ts


#test = False
test = True

rule_name = 'TripleTopClose'

print(RuleConfig.rule[rule_name])

tt = GeneralAnalysis()
if test:
    tt.analysis(['603777'], rule_name)
else:
    stock_list = ts.get_today_all()['code']
    tt.analysis(stock_list, rule_name)
