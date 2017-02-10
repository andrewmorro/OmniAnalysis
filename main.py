from analysis.GeneralAnalysis import GeneralAnalysis
from analysis import RuleConfig
from analysis import Rule
import tushare as ts


#test = False
test = True


tt = GeneralAnalysis()
if test:
    stock_list = ts.get_today_all()['code']
    rule_name = 'TripleTopClose'
    rule = Rule.Rise(3,0.3)
    df = tt.analysisByRule(rule,stock_list,'2017-02-01')
    #df = tt.analysisByRule(rule,['000877'],'2017-02-01')
    #df = tt.analysisByRuleName(rule_name,['000877'],'2017-02-01')
    print(df)


else:
    stock_list = ts.get_today_all()['code']
    df_good = tt.analysisByRuleName('TripleTopClose',stock_list)
    df_bad = tt.analysisByRuleName('TripleTopCloseBad',stock_list)
    df_good.to_excel(r'F:\BaiduSync\trade\文档\总结\量化\{}.xlsx'.format(RuleConfig.rule['TripleTopClose']), sheet_name='sheet1')
    df_bad.to_excel(r'F:\BaiduSync\trade\文档\总结\量化\{}.xlsx'.format(RuleConfig.rule['TripleTopCloseBad']), sheet_name='sheet1')
