'''


'''
import pandas as pd
import time
from datasets import infomation,daily, trade_cal

class dailys(trade_cal.trade_cal):

    def __init__(self,api_name = 'daily'):
        super(dailys, self).__init__(api_name)
        self.ord_add = 'asc'
        self.ftime_name = 'trade_date'

        return

    def api_query(self):
        st = time.strftime("%Y%m%d",self.stdate)
        #self.eddate = time.strptime("2005-01-01", "%Y-%m-%d")
        ed = time.strftime("%Y%m%d",self.eddate)
        cd = trade_cal.i.data['cal_date']
        dts = cd.loc[(cd[0:].astype(str) >= st) & (cd[0:].astype(str) <= ed) & (trade_cal.i.data['is_open'].astype(bool))]

        df = pd.DataFrame()
        for dt in dts:
            df = df.append(other=self.pro.daily(trade_date=dt),ignore_index=True)
            # 频率 500 hz 0.12s
            self.sleep()

        return df
