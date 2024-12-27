import baostock as bs
import pandas as pd

def trade_dates():
    #### 登陆系统 ####
    lg = bs.login()

    #### 获取交易日信息 ####
    rs = bs.query_trade_dates(start_date="2017-01-01", end_date="2017-06-30")
    print('query_trade_dates respond error_code:' + rs.error_code)
    print('query_trade_dates respond  error_msg:' + rs.error_msg)

    #### 打印结果集 ####
    data_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields)

    #### 结果集输出到csv文件 ####
    result.to_csv("trade_dates.csv", encoding="gbk", index=False)
    print(result)

    #### 登出系统 ####
    bs.logout()
    return result

def save_code():
    #### 登陆系统 ####
    lg = bs.login()
    # 显示登陆返回信息
    print('login respond error_code:' + lg.error_code)
    print('login respond  error_msg:' + lg.error_msg)

    #### 获取证券信息 ####
    rs = bs.query_all_stock(day="2017-06-30")
    print('query_all_stock respond error_code:' + rs.error_code)
    print('query_all_stock respond  error_msg:' + rs.error_msg)

    #### 打印结果集 ####
    data_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields)

    #### 结果集输出到csv文件 ####
    result.to_csv("../datas/bao/all_stock.csv", encoding="utf-8", index=False)
    print(result)

    #### 登出系统 ####
    bs.logout()

def save_k():
    # 登录 baostock
    bs.login()

    # 获取所有股票的基本信息
    stock_rs = bs.query_stock_basic()
    if stock_rs.error_code != '0':
        print(f"Error: {stock_rs.error_msg}")
        exit()

    # 获取上证股票代码
    sh_stock_list = []
    while stock_rs.next():
        stock = stock_rs.get_row_data()
        if stock[0].startswith('sh'):  # 股票代码以 'sh' 开头表示上证股票
            sh_stock_list.append(stock[0])

    # 设置保存目录
    output_dir = "../datas/bao/"
    os.makedirs(output_dir, exist_ok=True)

    # 下载每只股票的数据并保存为 CSV
    for ts_code in sh_stock_list:
        print(f"Downloading data for {ts_code}...")
        rs = bs.query_history_k_data_plus(
            ts_code,
            "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST",
            start_date="1990-01-01",  # 根据需要修改起始日期
            end_date="2024-12-31",
            frequency="d",  # 日频率
            adjustflag="3",  # 不复权
        )
        if rs.error_code != '0':
            print(f"Failed to fetch data for {ts_code}: {rs.error_msg}")
            continue

        data_list = []
        while rs.next():
            data_list.append(rs.get_row_data())

        # 转换为 DataFrame
        df = pd.DataFrame(data_list, columns=rs.fields)

        # 保存到 CSV
        file_path = os.path.join(output_dir, f"{ts_code}.csv")
        df.to_csv(file_path, index=False)
        print(f"Data for {ts_code} saved to {file_path}")

    # 登出 baostock
    bs.logout()

    print("All data downloaded successfully!")
