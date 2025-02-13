from matplotlib import font_manager
import matplotlib.pyplot as plt
import mplfinance as mpf
import pandas as pd

# 手动加载字体文件
font_path = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
font_manager.fontManager.addfont(font_path)
font_prop = font_manager.FontProperties(fname=font_path)
font_name = font_prop.get_name()

# 设置Matplotlib全局字体
plt.rcParams['font.sans-serif'] = [font_name]
plt.rcParams['axes.unicode_minus'] = False

# 创建自定义样式，强制指定字体
custom_style = mpf.make_mpf_style(base_mpl_style='default', rc={'font.family': 'sans-serif', 'font.sans-serif': [font_name]})

# 示例数据
data = pd.DataFrame({
    'Date': ['2023-01-01', '2023-01-02', '2023-01-03'],
    'Open': [100, 102, 101],
    'High': [103, 104, 103],
    'Low': [99, 100, 99],
    'Close': [101, 103, 102]
})
data['Date'] = pd.to_datetime(data['Date'])
data.set_index('Date', inplace=True)

# 使用自定义样式绘制K线图
mpf.plot(data, type='candle', title='示例K线图', ylabel='价格', style=custom_style)