import pandas as pd
from pytdx.hq import TdxHq_API
from datetime import datetime, timedelta

def connet():
    api = TdxHq_API()
    # if api.connect('119.147.212.81', 7709):  # 直接使用 if 判断连接是否成功
    if api.connect('222.73.139.166', 7709):  # 直接使用 if 判断连接是否成功
        return  api
    else:
        print("连接失败，请检查服务器地址和端口。")
        return None

def save_stocklist():
    # 参数说明

    # market(int):
    # 表示市场类型。
    # 1：上证市场（沪市）。
    # 0：深证市场（深市）。
    # 2：其他市场（如创业板）。

    # offset(int):
    # 表示获取数据的起始位置（偏移量）。
    # 该值通常从 0 开始，表示从第一条数据开始获取。
    # 由于数据是分批获取的，您可以通过增加该值来获取后续的数据。例如，100
    # 表示从第101条数据开始获取。

    # 获取数据
    api = connet()
    if api == None:
       exit
    # 获取代码列表
    market = 0
    stock_list = pd.DataFrame()
    # for market in [0, 1]:
    i = 0
    while True:  # 每次获取 100 个股票，最多可获取 100 * 200 = 20,000 个
        data = api.get_security_list(market, i * 100)
        if not data:  # 如果没有数据返回，结束循环
            print(i)
            break
        stock_list = pd.concat([stock_list, pd.DataFrame(data)], ignore_index=True)
        i = i +1
    stock_list.to_csv('../datas/sz/stock_list.csv')

    market = 1
    stock_list = pd.DataFrame()
    i = 0
    while True:  # 每次获取 100 个股票，最多可获取 100 * 200 = 20,000 个
        data = api.get_security_list(market, i * 100)
        if not data:  # 如果没有数据返回，结束循环
            print(i)
            break
        stock_list = pd.concat([stock_list, pd.DataFrame(data)], ignore_index=True)
        i = i + 1
    stock_list.to_csv('../datas/sh/stock_list.csv')

    # data = api.get_k_data('000001', '2015-01-01', '2015-12-31')
    api.disconnect()  # 手动断开连接

def get_stocklist(market):
    # 假设您的DataFrame名为stock_list，并且它包含一个名为'code'的列
    if market == 1 :
        stock_list = pd.read_csv('../datas/sh/stock_list.csv')
        # 确保'code'列是字符串类型
        stock_list['code'] = stock_list['code'].astype(str)

        # 筛选出以'00'和'30'开头的股票代码
        filtered_stocks = stock_list[stock_list['code'].str.startswith(('00', '30'))]
        # 去除 'code' 列的重复项
        filtered_stocks = filtered_stocks.drop_duplicates(subset='code', keep='first')

        # # 打印结果
        # print(filtered_stocks)
    else:
        stock_list = pd.read_csv('../datas/sz/stock_list.csv', dtype={'code': str})
        # 确保'code'列是字符串类型
        # stock_list['code'] = stock_list['code'].astype(str)

        # 筛选出以'00'和'30'开头的股票代码
        filtered_stocks = stock_list[stock_list['code'].str.startswith(('00', '30'))]
        # 去除 'code' 列的重复项
        filtered_stocks = filtered_stocks.drop_duplicates(subset='code', keep='first')
        # filtered_stocks = stock_list[stock_list['code'].str.startswith(('30'))]
        # filtered_stocks['code'] = filtered_stocks['code'].astype(str)

        # 打印结果
        # print(filtered_stocks)
    return filtered_stocks

api = connet()

def save_k(market,code,start_date,end_date):
    data = api.get_k_data(code, start_date, end_date)
    # 将数据转换为DataFrame
    df = pd.DataFrame(data)
    if market == 1:
        df.to_csv('../datas/sh/day/'+code+'.csv')
    else:
        df.to_csv('../datas/sz/day/' + code + '.csv')

def get_xdxr_factors(market,code):
    #除权因子
    ordered_dict_list = api.get_xdxr_info(market, code)
    # print(ordered_dict_list)
    # 初始化DataFrame
    # 初始化DataFrame
    xdxr_factors = pd.DataFrame(columns=['date', 'single_factor'])

    # 遍历除权信息
    for idx, item in enumerate(ordered_dict_list):
        year = item['year']
        month = item['month']
        day = item['day']
        fenhong = item['fenhong']
        peigujia = item['peigujia']
        songzhuangu = item['songzhuangu']
        peigu = item['peigu']

        # 计算单个除权事件的复权因子
        cash_dividend_factor = 1.0 if fenhong is None else 1 + fenhong
        rights_issue_factor = 1.0 if peigujia is None else 1 + peigujia
        bonus_issue_factor = 1.0 if songzhuangu is None else 10 / (10 + songzhuangu)

        # 计算总的复权因子
        single_factor = 1.0 / (cash_dividend_factor * rights_issue_factor * bonus_issue_factor)

        # 将数据添加到DataFrame中
        xdxr_factors.loc[idx] = [pd.to_datetime(f'{year}-{month:02d}-{day:02d}'), single_factor]

    # 打印DataFrame
    # print(xdxr_factors)
    # 确保xdxr_factors是按日期排序的
    xdxr_factors = xdxr_factors.sort_values(by='date')
    return xdxr_factors

def load_k(market,code,start_date,end_date):
    if market == 1 :
        stock_k = pd.read_csv('../datas/sh/day/'+code+'.csv')
    else:
        stock_k = pd.read_csv('../datas/sz/day/' + code + '.csv')

    stock_k = stock_k[(stock_k['date'] >= start_date) & (stock_k['date'] <= end_date)]

    # print(stock_k)
    return stock_k

def get_k(market,code,start_date,end_date):
    # 前复权
    # xdxr_factors = get_xdxr_factors(market,code)

    df_stock = load_k(market,code,start_date,end_date)

    # 将日期列设置为索引，并确保它是DatetimeIndex类型
    # df_stock['date'] = pd.to_datetime(df_stock['date'])
    # df_stock.set_index('date', inplace=True)
    # 初始化前复权收盘价列
    # df_stock['close_adj'] = 0.0
    #
    # 应用复权因子到收盘价
    # for idx, row in xdxr_factors.iterrows():
    #     mask = df_stock.index >= row['date']
    #     df_stock.loc[mask, 'close_adj'] = df_stock.loc[mask, 'close'] / row['single_factor']

    # 打印前复权后的DataFrame
    # print(df_stock)
    return df_stock

def get_k_back(market,code,start_date,end_date):
    #后复权
    xdxr_factors = get_xdxr_factors(market,code)

    df_stock = load_k(market,code,start_date,end_date)

    # 将日期列设置为索引，并确保它是DatetimeIndex类型
    df_stock['date'] = pd.to_datetime(df_stock['date'])
    df_stock.set_index('date', inplace=True)
    # 初始化前复权收盘价列
    df_stock['close_adj'] = 0.0

    # 应用复权因子到收盘价
    for idx, row in xdxr_factors.iterrows():
        mask = df_stock.index >= row['date']
        df_stock.loc[mask, 'close_adj'] = df_stock.loc[mask, 'close'] * row['single_factor']

    # 打印前复权后的DataFrame
    # print(df_stock)
    return df_stock

def save_ks(market,start_date,end_date):
    # 获取数据
    stock_list = get_stocklist(0)
    for code in stock_list['code']:
        # code = stock_list['code'].iloc[i]
        save_k(market,code,start_date,end_date)
        # if code == '301633':
        #     print(code)
        # print(code)
    api.disconnect()  # 手动断开连接


if __name__ == '__main__':
    # save_stocklist()
    # get_stocklist(0)
    # save_k(0,'301633','2024-01-01','2024-12-31')
    # save_k(0,'301585','2024-01-01','2024-12-31')
    # save_ks(0,'2024-01-01','2024-12-31')
    # save_k(0,'000001','1991-05-15','2024-12-31')
    # save_k(0,'000001','2019-01-01','2024-12-31')
    # save_ks(1,'2024-01-01','2024-12-31')
    get_k(0,'000001','1991-05-15','2024-12-31')

