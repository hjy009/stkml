

# 导入tushare
import tushare as ts
# 初始化pro接口
pro = ts.pro_api('47b9a627f1563898aa332944ec91cc01218dda39d996ab2f2fe9e507')

# 拉取数据
df = pro.daily(**{
    "ts_code": "000001.sz",
    "trade_date": "",
    "start_date": "",
    "end_date": "",
    "offset": "",
    "limit": ""
}, fields=[
    "ts_code",
    "trade_date",
    "open",
    "high",
    "low",
    "close",
    "pre_close",
    "change",
    "pct_chg",
    "vol",
    "amount"
])
print(df)


