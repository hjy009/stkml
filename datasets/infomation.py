#import pandas as pd
import numpy as np
import time
from datasets import infomations
#from reportlab.lib.normalDate import today

class infomation:
    api_name = ''
    info = None
    stdate = time.strptime("1990-12-19", "%Y-%m-%d")
    eddate = time.strptime("1990-12-19", "%Y-%m-%d")
    ltdate = time.strptime("1990-12-19", "%Y-%m-%d")
    fdate = time.strptime("1990-12-19", "%Y-%m-%d")

    def __init__(self,api_name = 'infomation'):
        if len(api_name) ==0:
            self.api_name = type(self).__name__
        else:
            self.api_name = api_name
        self.info = infomations.i.read_key(self.info_key())
        self.load_info()
        return

    def info_key(self):
        res = self.api_name
        return res

    def load_info(self):
        self.stdate = time.strptime(self.info.loc['start_date'], "%Y-%m-%d %H:%M:%S")
        self.eddate = time.strptime(self.info.loc['end_date'], "%Y-%m-%d %H:%M:%S")
        self.ltdate = time.strptime(self.info.loc['list_date'], "%Y-%m-%d %H:%M:%S")
        self.fdate = time.strptime(self.info.loc['file_date'], "%Y-%m-%d %H:%M:%S")
        return

    def load_data(self):
        self.stdate = time.localtime()
        self.eddate = time.localtime()
        return

    def save_info(self):
        self.info.at['start_date'] = time.strftime("%Y-%m-%d %H:%M:%S",self.stdate)
        self.info.at['end_date'] = time.strftime("%Y-%m-%d %H:%M:%S",self.eddate)
        self.info.at['list_date'] = time.strftime("%Y-%m-%d %H:%M:%S",self.ltdate)
        self.info.at['file_date'] = time.strftime("%Y-%m-%d %H:%M:%S",self.fdate)
        infomations.i.write_key(self.info_key(), self.info)
        return

    def init(self):
        self.load_info()
        self.load_data()
        self.save_info()
        return

    def inttotime(self,it):
        dt = time.strptime(np.str(it), '%Y%m%d')
        return dt

    def inttoftime(self,it):
        dt = time.strptime(np.str(int(it)),'%Y%m%d')
        str = time.strftime("%Y-%m-%d %H:%M:%S",dt)
        return str
