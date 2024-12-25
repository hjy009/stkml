import pandas as pd
import numpy as np
import os,time
from datasets import paths

class infomations:
    data = None
    file_path = ''
    modified = False
    dCols = ['infomation','start_date','end_date','list_date','file_date']
    dDef = ['','1990-12-19 00:00:00','1990-12-19 00:00:00','1990-12-19 00:00:00','1990-12-19 00:00:00']

    #用__new__实现单例模式
    def __new__(cls, *args, **kwargs):
        if not '_instance' in vars(cls):
            #print 'creating instance of Singleton1'
            cls._instance = super(infomations, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.file_path = paths.get_infopath()
        if not os.path.exists(self.file_path):
            self.data = pd.DataFrame(data=[], columns=self.dCols)
            self.data.to_csv(path_or_buf=self.file_path, index_label='key')
        else:
            self.load_file()
        return

    def __del__(self):
        if self.modified :
            #self.save_file()
            print('%s 调用__del__() 没有保存对象' % (type(self).__name__))
        #print("infomations调用__del__() 销毁对象，释放其空间")
        #super(infomations, self).__del__(self)

    def load_file(self):
        self.data = pd.read_csv(filepath_or_buffer=self.file_path, index_col=0)
        return

    def save_file(self):
        self.data.to_csv(path_or_buf=self.file_path, index_label='key')
        self.modified = False
        return

    def read_key(self,key):
        try:
            res = self.data.loc[key]
        except:
            res = pd.Series(data=self.dDef,index=self.dCols)
        return res

    def write_key(self,key,ss):
        #self.load_file()
        self.data.loc[key] = ss
        self.modified = True
        #self.save_file()
        return

#必须单线程使用 infos
i = infomations()