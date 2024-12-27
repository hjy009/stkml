import backtrader as bt
import pandas as pd
import numpy as np
from pytdx.hq import TdxHq_API
from datetime import datetime
from transformer import baomodel as bm

def conv():
    # 读取原始 CSV 文件
    file_path = "../datas/bao/sh.600000.csv"
    df = pd.read_csv(file_path)

    # 转换为 Backtrader 格式
    df_bt = df[['date', 'open', 'high', 'low', 'close', 'volume']].copy()
    df_bt.rename(columns={'date': 'datetime'}, inplace=True)

    # 添加 openinterest 列，填充为 0
    df_bt['openinterest'] = 0

    # 保存为新的 CSV 文件，供 Backtrader 使用
    output_path = "../datas/bao/sh.600000_bt.csv"
    df_bt.to_csv(output_path, index=False)

    print(f"Converted file saved to {output_path}")

# conv()

model = bm.TransformerLanguageModel()
model = model.to(bm.device)
model.eval()


class PredictNextIndicator(bt.Indicator):
    lines = ('prediction',)  # 定义输出线，预测值
    params = (('context_length', 5),)  # 参数：上下文长度

    def __init__(self):
        # 确保有足够的数据供上下文使用
        self.addminperiod(self.params.context_length)

    def next(self):
        # 获取最近 context_length 个数据
        recent_data = np.array(self.data.get(size=self.params.context_length))

        # 预测逻辑：简单示例，用均值作为预测
        predicted_value = np.mean(recent_data)

        # start_ids = np.random.random_integers(0, 2001, bm.context_length)
        # x = (torch.tensor(start_ids, dtype=torch.long, device=bm.device)[None, ...])
        # y = model.generate(x, max_new_tokens=1)

        # 输出到指标线
        self.lines.prediction[0] = predicted_value


# 测试策略
class TestStrategy(bt.Strategy):
    def __init__(self):
        # 将自定义指标应用于数据源
        self.pred_indicator = PredictNextIndicator(self.data, context_length=5)

    def next(self):
        # 打印当前时刻的预测值和实际值
        print(f'Date: {self.datas[0].datetime.date(0)}, '
              f'Predicted: {self.pred_indicator.prediction[0]:.2f}, '
              f'Actual: {self.data[0]:.2f}')


# 定义简单均线策略
class SimpleSmaStrategy(bt.Strategy):
    params = (('short_period', 10), ('long_period', 30))

    def __init__(self):
        self.short_sma = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.short_period)
        self.long_sma = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.long_period)
        # 将自定义指标应用于数据源
        self.pred_indicator = PredictNextIndicator(self.data.close, context_length=5)

    def next(self):
        if self.short_sma > self.long_sma and not self.position:
            self.buy()  # 买入
        elif self.short_sma < self.long_sma and self.position:
            self.sell()  # 卖出
        # 打印当前时刻的预测值和实际值
        print(f'Date: {self.datas[0].datetime.date(0)}, '
              f'Predicted: {self.pred_indicator.prediction[0]:.2f}, '
              f'Actual: {self.data[0]:.2f}')

# 初始化 Backtrader 环境
cerebro = bt.Cerebro()

# 加载数据
data = bt.feeds.GenericCSVData(
    dataname="../datas/bao/sh.600000_bt.csv",
    dtformat='%Y-%m-%d',
    timeframe=bt.TimeFrame.Days,
    compression=1,
    openinterest=-1
)
cerebro.adddata(data)

# 添加策略
cerebro.addstrategy(SimpleSmaStrategy)

# 设置初始资金
cerebro.broker.setcash(100000.0)

# 启动回测
print("Starting Portfolio Value: %.2f" % cerebro.broker.getvalue())
cerebro.run()
print("Ending Portfolio Value: %.2f" % cerebro.broker.getvalue())

# 绘制结果
cerebro.plot()
