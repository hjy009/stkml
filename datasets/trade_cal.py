"""

交易日历

接口：trade_cal
描述：获取各大交易所交易日历数据,默认提取的是上交所

输入参数
名称     类型     必选     描述
exchange     str     N     交易所 SSE上交所 SZSE深交所
start_date     str     N     开始日期
end_date     str     N     结束日期
is_open     str     N     是否交易 '0'休市 '1'交易

输出参数
名称     类型     默认显示     描述
exchange     str     Y     交易所 SSE上交所 SZSE深交所
cal_date     str     Y     日历日期
is_open     str     Y     是否交易 0休市 1交易
pretrade_date     str     N     上一个交易日

接口示例


pro = ts.pro_api()


pro.trade_cal(exchange='', start_date='20180101', end_date='20181231')

或者


pro.query('trade_cal', start_date='20180101', end_date='20181231')

数据样例

    exchange  cal_date  is_open
0           SSE  20180101        0
1           SSE  20180102        1
2           SSE  20180103        1
3           SSE  20180104        1
4           SSE  20180105        1
5           SSE  20180106        0
6           SSE  20180107        0
7           SSE  20180108        1
8           SSE  20180109        1
9           SSE  20180110        1
10          SSE  20180111        1
11          SSE  20180112        1
12          SSE  20180113        0
13          SSE  20180114        0
14          SSE  20180115        1
15          SSE  20180116        1
16          SSE  20180117        1
17          SSE  20180118        1
18          SSE  20180119        1
19          SSE  20180120        0
20          SSE  20180121        0

"""
import tushare as ts
from datasets import stock_basic
import time
import pandas as pd

class trade_cal(stock_basic.stock_basic):

    ord_add = 'idx'  #idx,asc,des

    def __init__(self,api_name = 'trade_cal'):
        super(trade_cal, self).__init__(api_name)
        self.ftime_name = 'cal_date'
        #self.load_file()
        return

    def api_query(self):
        df = self.pro.query('trade_cal',
                            start_date=time.strftime("%Y%m%d", self.stdate),
                            end_date=time.strftime("%Y%m%d", self.eddate))
        if len(df)>0:
            df.index = df[self.ftime_name].astype('datetime64')
        return df

    def append_data(self,df):
        if len(self.data) == 0:
            super(trade_cal, self).append_data(df)
        else:
            if len(df) >0 :
                if self.ord_add == 'idx':
                    self.data = df.combine_first(self.data)
                else:
                    st = time.strftime("%Y%m%d", self.stdate)
                    self.data.drop(index=self.data.loc[self.data[self.ftime_name].astype(str) >= st].index,
                                   inplace=True)
                    if self.ord_add == 'asc':
                        # self.data.drop(labels=self.data.index[[len(self.data)-1]],inplace=True)
                        self.data = self.data.append(other=df, ignore_index=True)
                    else:
                        # self.data.drop(labels=self.data.index[[0]], inplace=True)
                        self.data = df.append(other=self.data, ignore_index=True)
        return

    def k5(self,start,end,is_open=1):
        #5000行限制，分割
        df = self.data.loc[(self.data['cal_date'].astype(str)>=start)
                           &(self.data['cal_date'].astype(str)<=end)
                           &(self.data['is_open'].astype(int)==is_open)]
        a,b = divmod(len(df),5000)
        res = []
        for i in range(a):
            res.append([str(int(df['cal_date'].iloc[i])),str(int(df['cal_date'].iloc[i+5000-1]))])
            #res.append([df['cal_date'].iloc[i].astype(str),df['cal_date'].iloc[i+5000-1].astype(str)])
            #print(i,df['cal_date'].iloc[i],i+5000-1,df['cal_date'].iloc[i+5000-1])
        if b>0:
            res.append([str(int(df['cal_date'].iloc[a * 5000])),str(int(df['cal_date'].iloc[a * 5000 + b - 1]))])
            #res.append([df['cal_date'].iloc[a * 5000].astype(str),df['cal_date'].iloc[a * 5000 + b - 1].astype(str)])
            #print(a * 5000, df['cal_date'].iloc[a * 5000], a * 5000 + b - 1, df['cal_date'].iloc[a * 5000 + b - 1])
        #print(res)
        return res

def date_range(from_date,to_date,is_open=10):
    '''
    df = i.data.loc[from_date:to_date,:]
    df = df.loc[df[is_open]==is_open]
    arr = df[i.ftime_name].values
    '''
    df = i.data
    if is_open==10:
        df = df.loc[(df[i.ftime_name].astype(str) >= from_date) &
                    (df[i.ftime_name].astype(str) <= to_date)
                    ]
    else:
        df = df.loc[(df[i.ftime_name].astype(str) >= from_date) &
                    (df[i.ftime_name].astype(str) <= to_date) &
                    (df['is_open'] == is_open)
                    ]
    arr = df[i.ftime_name].values
    return arr

i = trade_cal()
