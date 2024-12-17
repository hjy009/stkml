import backtrader as bt
import pandas as pd
from pytdx.hq import TdxHq_API
from datetime import datetime

# 获取数据
api = TdxHq_API()
# if api.connect('119.147.212.81', 7709):  # 直接使用 if 判断连接是否成功
if api.connect('222.73.139.166', 7709):  # 直接使用 if 判断连接是否成功

    data = api.get_k_data('000001', '2015-01-01', '2015-12-31')
    api.disconnect()  # 手动断开连接
else:
    print("连接失败，请检查服务器地址和端口。")

# 将数据转换为DataFrame
df = pd.DataFrame(data)

# 将数据转换为Backtrader的数据格式
class TdxData(bt.feeds.PandasData):
    params = (
        ('datetime', 'date'),
        ('open', 'open'),
        ('high', 'high'),
        ('low', 'low'),
        ('close', 'close'),
        ('volume', 'vol'),
        ('openinterest', -1),
    )

# 将日期列转换为datetime格式
df['date'] = pd.to_datetime(df['date'])

# 创建Backtrader数据源
data = TdxData(dataname=df)

# 创建策略
class MyStrategy(bt.Strategy):
    def __init__(self):
        pass

    def next(self):
        if not self.position:
            if self.data.close[0] > self.data.open[0]:
                self.buy(size=100)
        elif self.data.close[0] < self.data.open[0]:
            self.sell(size=100)

# 创建Cerebro引擎
cerebro = bt.Cerebro()
cerebro.adddata(data)
cerebro.addstrategy(MyStrategy)
cerebro.broker.set_cash(100000)

# 运行回测
cerebro.run()
cerebro.plot()
