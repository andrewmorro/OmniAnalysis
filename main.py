from analysis.GeneralAnalysis import GeneralAnalysis
from analysis import RuleConfig
import tushare as ts


test = False
#test = True

rule_name = 'TripleTopClose'

tt = GeneralAnalysis()
if test:
    df = tt.analysis(['603777'], rule_name)
else:
    stock_list = ts.get_today_all()['code']
    df_good = tt.analysis(stock_list, 'TripleTopClose')
    df_bad = tt.analysis(stock_list, 'TripleTopCloseBad')
    df_good.to_excel(r'F:\BaiduSync\trade\文档\总结\量化\{}.xlsx'.format(RuleConfig.rule['TripleTopClose']), sheet_name='sheet1')
    df_bad.to_excel(r'F:\BaiduSync\trade\文档\总结\量化\{}.xlsx'.format(RuleConfig.rule['TripleTopCloseBad']), sheet_name='sheet1')
