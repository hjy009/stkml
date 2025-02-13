import mplfinance as mpf
import akshare as ak
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.font_manager as fm

# 指定 Microsoft YaHei 字体路径
font_path = '/usr/share/fonts/msfont/msyh.ttf'  # 替换为您的字体文件路径
font_prop = fm.FontProperties(fname=font_path)

# 设置字体
matplotlib.rcParams['font.sans-serif'] = font_prop.get_name()
matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 获取股票历史数据
stock_data = ak.stock_zh_a_hist(symbol="000001", period="daily", start_date="20230101", end_date="20231231")
stock_data.set_index('日期', inplace=True)

# 将索引转换为 DatetimeIndex
stock_data.index = pd.to_datetime(stock_data.index)

print(stock_data.columns)
print(len(stock_data.columns))

# 为所有列重新命名
stock_data.columns = [
    "Stock Code", "Open", "Close", "High", "Low",
    "Volume", "Amount", "Amplitude", "Change Percentage", "Change Amount", "Turnover Rate"
]

# 绘制K线图
mpf.plot(stock_data, type='candle', volume=True, style='yahoo', title="平安银行 K 线图")
