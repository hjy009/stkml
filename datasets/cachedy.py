'''


'''
import time,math,pandas as pd
from datasets import dailys,stock_basic,daily,trade_cal,infomations
#from reportlab.lib.normalDate import today

class cachedy(dailys.dailys):

    def __init__(self,api_name = 'daily.cache',start_date = ''):
        super(cachedy, self).__init__(api_name)
        if start_date == '':
            #self.stdate = time.strptime(
            #    infomations.i.data.loc[infomations.i.data.index.astype(str).str.contains('daily')]['start_date'].max(),
            #    "%Y-%m-%d %H:%M:%S"
            #    )
            self.info.at['start_date'] = infomations.i.data.loc[infomations.i.data.index.astype(str).str.contains('daily')]['start_date'].max()
        return

    def load_data(self):
        #super(cachedy, self).load_data()
        self.data = pd.DataFrame()
        self.load_api()
        self.save_fdate()
        #self.save_all()
        return

    def save_dailys(self):
        if len(self.data)==0:
            self.load_file()
        st = time.strftime("%Y%m%d", self.ltdate)
        dys = dailys.dailys()
        dys.load_file()
        if time.strftime("%Y%m%d", dys.eddate) >= st:
            dys.stdate = self.ltdate
            dys.eddate = self.eddate
            dys.after_query(self.data)
            print(['append', 'dailys'])
        else:
            dys.init()
            print(['init', 'dailys'])
        return

    def save_dailyx(self):
        #infomations.infos.infos.loc[infomations.infos.infos.index.str.contains('daily.')]
        if len(self.data)==0:
            self.load_file()
        st = time.strftime("%Y%m%d", self.ltdate)

        stb = stock_basic.i
        for tc in stb.data['ts_code']:
            dy = daily.daily(ts_code=tc)
            dy.load_file()
            if (len(dy.data)>0) & (time.strftime("%Y%m%d",dy.eddate) >= st):
                df = self.data.loc[self.data['ts_code']==tc].sort_values(by='trade_date',ascending=False,ignore_index=True)
                if len(df) > 0:
                    df.index = df[dy.ftime_name].astype(str).astype('datetime64[ns]')
                else:
                    continue
                dy.stdate = self.ltdate
                dy.eddate = self.eddate
                dy.after_query(df)
                print(['append',tc])
            else:
                dy.init()
                print(['init',tc])
        return

    def save_all_fdate(self):
        stb = stock_basic.i
        for tc in stb.data['ts_code']:
            dy = daily.daily(ts_code=tc)
            dy.save_fdate()
            print(['save fdate', tc,time.strftime('%Y-%m-%d',dy.fdate)])
        return

    def save_allx(self):
        stb = stock_basic.i
        for tc in stb.data['ts_code']:
            dy = daily.daily(ts_code=tc)
            dy.load_file()
            if len(dy.data)>0:
                dy.data.index = dy.data[self.ftime_name].astype('str').astype('datetime64[ns]')
                dy.save_file()
                print(['save ', tc,time.strftime('%Y-%m-%d',dy.fdate)])
        return

    def save_all_ltdate(self):
        stb = stock_basic.i
        for tc in stb.data['ts_code']:
            dy = daily.daily(ts_code=tc)
            base_list = stock_basic.list_date(tc)
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