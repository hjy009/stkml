import tushare as ts
from datasets import stock_basic, trade_cal, new_share, pro_bar, daily, dailys, adj_factor
from datetime import date
import numpy as np

class tusets:
    stb = None
    tdc = None
    stcs = None
    
#    adj = adj_factor.adj_factor()
#    nsh = new_share.new_share()
#    dts = stock_code.stock_code()

    def __init__(self):

        return
    
    def stb_save_all(self):
        self.stb = stock_basic.stock_basic()
        self.tdc = trade_cal.trade_cal()
        self.stcs = dailys.dailys()

        return

    def tdc_save_all(self):
        self.tdc = trade_cal.trade_cal()
        return
    
    def stc_save_all(self):
        #self.stcs.refresh_dates(self.stb)
#        self.stcs.load_buf('20191205')
#        self.stcs.append_bybuf()

        self.stcs.refresh_mindate('000001.SH')
        #self.stcs.save_file()
        '''
        idx = 0
        while idx < len(self.stb.data['values']) :
            ts_code = self.stb.data['values'][idx][0]
            list_date = self.stb.data['values'][idx][11] 
            print(ts_code,list_date)
            self.stc = stock_code.stock_code(ts_code=ts_code)
            idx += 1    
        '''
        return
    
    def save_all(self):
        self.stb_save_all()
        self.tdc_save_all()
        self.stc_save_all()
        return

    def save_fdate(self):
        stb = stock_basic.stock_basic()
        stb.save_fdate()
        tdc = trade_cal.trade_cal()
        tdc.save_fdate()
        dys = dailys.dailys()
        dys.save_fdate()
        return