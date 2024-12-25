import numpy as np
import pandas as pd
import os
import time
from datasets import dailys,stock_basic,daily,trade_cal

class ccdy():
    dys = {}

    def df_stock(self,ts_code):
        if ts_code not in self.dys:
            self.dys[ts_code] = daily.daily(ts_code=ts_code)
            self.dys[ts_code].load_file()
        df = self.dys[ts_code].data
        return df

    def df_stdate(self,ts_code,from_date,to_date):
        df = self.df_stock(ts_code)
        df = df.loc[(df['trade_date'].astype(float) >= float(from_date)) & (df['trade_date'].astype(float) <= float(to_date))]
        return df

    def valuebykey(self,ts_code,st_date,key):
        df = self.df_stdate(ts_code,st_date,st_date)
        res = df[key].iloc[0]
        return  res

i = ccdy()