from analysis.GeneralAnalysis import GeneralAnalysis
from analysis import RuleConfig
from analysis import Rule
import tushare as ts
import datetime

#test = False
test = True


tt = GeneralAnalysis()
if test:
    rule_name = 'FuelUp'
    #ts.get_today_all().to_excel(r'F:\BaiduSync\trade\总结\量化\stock_list.xlsx')
    #exit(0)

    stock_list = ts.get_today_all()['code']


    rise = Rule.Rise(3,0.3)
    notHori = Rule.NotHorizontalMulti(2)
    strategy = Rule.Strategy()
    strategy.addRule(rise)
    strategy.addRule(notHori)

    #df = tt.analysisByRule(strategy,stock_list,'2017-02-01')

    df = tt.analysisByRuleName(rule_name,stock_list,'2017-01-01')

    #df = tt.analysisByRuleName(rule_name, stock_list,'2017-01-01')
    print(df)
    df.to_excel(r'F:\BaiduSync\trade\总结\量化\{}-{}.xlsx'.format(RuleConfig.rule[rule_name],datetime.datetime.now().strftime('%Y-%m-%d')), sheet_name=RuleConfig.rule[rule_name])


else:
    stock_list = ts.get_today_all()['code']
    df_good = tt.analysisByRuleName('TripleTopClose',stock_list)
    df_bad = tt.analysisByRuleName('TripleTopCloseBad',stock_list)
    df_good.to_excel(r'F:\BaiduSync\trade\文档\总结\量化\{}.xlsx'.format(RuleConfig.rule['TripleTopClose']), sheet_name='sheet1')
    df_bad.to_excel(r'F:\BaiduSync\trade\文档\总结\量化\{}.xlsx'.format(RuleConfig.rule['TripleTopCloseBad']), sheet_name='sheet1')
