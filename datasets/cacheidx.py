'''


'''
import time,math
import pandas as pd
from datasets import index_basic,index_daily,trade_cal
#from reportlab.lib.normalDate import today

class cacheidx(trade_cal.trade_cal):

    def __init__(self,api_name = 'index.cache'):
        super(cacheidx, self).__init__(api_name)
        self.ftime_name = 'trade_date'
        return


    def api_query(self):
        df = pd.DataFrame()
        return df

    def save_dailyx(self,market):
        idb = index_basic.i.data.loc[(index_basic.i.data['market']==market)]
        for tc in idb['ts_code']:
            idx = index_daily.index_daily(ts_code=tc)
            idx.init()
        return

    def save_all_fdate(self):
        idb = index_basic.i
        for tc in idb.data['ts_code']:
            idx = index_daily.index_daily(ts_code=tc)
            idx.save_fdate()
            print(['save fdate', tc,time.strftime('%Y-%m-%d',idx.fdate)])
        return

    def save_ltdate(self,market):
        idb = index_basic.i.data.loc[(index_basic.i.data['market']==market)]
        for tc in idb['ts_code']:
            dy = index_daily.index_daily(ts_code=tc)
            base_list = index_basic.list_date(tc)
            dy.load_file()
            try:
                dy_list = dy.data[dy.ftime_name].astype(int).min()
            except:
                dy_list = 20210108
            dy.ltdate = dy.inttotime(base_list)
            if (dy_list-base_list)>90:
                dy.stdate = dy.ltdate
                dy.data = dy.api_query()
                dy.save_file()
                print(['save ltdate',tc, base_list,dy_list])
            dy.save_info()
        return