import pandas as pd
from pytdx.hq import TdxHq_API
from datetime import datetime

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

def get_k(market,code,start_date,end_date):
    if market == 1 :
        stock_k = pd.read_csv('../datas/sh/day/'+code+'.csv')
    else:
        stock_k = pd.read_csv('../datas/sz/day/' + code + '.csv')

    return stock_k


def save_ks(market,start_date,end_date):
    # 获取数据
    stock_list = get_stocklist(0)
    for code in stock_list['code']:
        # code = stock_list['code'].iloc[i]
        save_k(market,code,start_date,end_date)
        if code == '301633':
            print(code)
        print(code)
    api.disconnect()  # 手动断开连接



if __name__ == '__main__':
    # save_stocklist()
    # get_stocklist(0)
    # save_k(0,'301633','2024-01-01','2024-12-31')
    # save_k(0,'301585','2024-01-01','2024-12-31')
    # save_ks(0,'2024-01-01','2024-12-31')
    # save_k(0,'000001','2024-01-01','2024-12-31')
    save_k(0,'000001','2019-01-01','2024-12-31')
    # save_ks(1,'2024-01-01','2024-12-31')