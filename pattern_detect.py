import talib
from yahoo_fin.stock_info import *
from yahoo_fin.stock_info import get_analysts_info
import yahoo_fin.stock_info as si
import pandas as pd
data = get_data("ETH-USD",start_date="2020-01-01",end_date="2020-08-01",index_as_date=True,interval="1d")





morning_star = talib.CDLMORNINGSTAR(data['open'], data['high'], data['low'], data['close'], penetration=0)

# print(morning_star[morning_star != 0])

engulfing = talib.CDLENGULFING(data['open'], data['high'], data['low'], data['close'])

data['Morning_Star'] = morning_star
data['Engulfing'] = engulfing

engulfing_days = data[data['Engulfing'] != 0]
print(engulfing_days)









