"""

复权因子

接口：adj_factor
更新时间：早上9点30分
描述：获取股票复权因子，可提取单只股票全部历史复权因子，也可以提取单日全部股票的复权因子。

输入参数
名称     类型     必选     描述
ts_code     str     Y     股票代码
trade_date     str     N     交易日期(YYYYMMDD，下同)
start_date     str     N     开始日期
end_date     str     N     结束日期

注：日期都填YYYYMMDD格式，比如20181010

输出参数
名称     类型     描述
ts_code     str     股票代码
trade_date     str     交易日期
adj_factor     float     复权因子

接口示例


pro = ts.pro_api()

#提取000001全部复权因子
df = pro.adj_factor(ts_code='000001.SZ', trade_date='')


#提取2018年7月18日复权因子
df = pro.adj_factor(ts_code='', trade_date='20180718')

或者


df = pro.query('adj_factor',  trade_date='20180718')

数据样例

        ts_code trade_date  adj_factor
0     000001.SZ   20180809     108.031
1     000001.SZ   20180808     108.031
2     000001.SZ   20180807     108.031
3     000001.SZ   20180806     108.031
4     000001.SZ   20180803     108.031
5     000001.SZ   20180802     108.031
6     000001.SZ   20180801     108.031
7     000001.SZ   20180731     108.031
8     000001.SZ   20180730     108.031
9     000001.SZ   20180727     108.031
10    000001.SZ   20180726     108.031
11    000001.SZ   20180725     108.031
12    000001.SZ   20180724     108.031
13    000001.SZ   20180723     108.031
14    000001.SZ   20180720     108.031
15    000001.SZ   20180719     108.031
16    000001.SZ   20180718     108.031
17    000001.SZ   20180717     108.031
18    000001.SZ   20180716     108.031
19    000001.SZ   20180713     108.031
20    000001.SZ   20180712     108.031

"""
import tushare as ts
from datasets import stock_basic, daily

class adj_factor(daily.daily):
    
    def __init__(self,api_name = 'adj_factor',ts_code='000001.SZ'):
        self.init(api_name,ts_code)
        return
    
    def run_api(self,start_date, end_date):
        pro = ts.pro_api()
        df = pro.adj_factor(ts_code=self.ts_code, trade_date='')
        return df

    def get_codedateID(self):
        return 1
 
def save_all():
    stb = stock_basic.stock_basic()
    idx = 0
    while idx < len(stb.data['values']) :
        ts_code = stb.data['values'][idx][0]
        list_date = stb.data['values'][idx][11] 
        print(ts_code,list_date)
        adj_factor(ts_code=ts_code)
        idx += 1
    
    return

