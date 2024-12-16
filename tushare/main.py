# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import tushare as ts

# 设置tushare pro的token信息，需要在tushare pro网站申请
ts.set_token('47b9a627f1563898aa332944ec91cc01218dda39d996ab2f2fe9e507')

# 初始化pro接口
pro = ts.pro_api()

# 获取000001股票在20180810的日线行情数据
df = pro.daily(ts_code='000001.SH', trade_date='20180810')

print(df)

# Press the green button in the gutter to run the script.
#if __name__ == '__main__':
    #print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
