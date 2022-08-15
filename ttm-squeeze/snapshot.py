import os
# import request and API data download
from yahoo_fin.stock_info import *
from yahoo_fin.stock_info import get_analysts_info
import yahoo_fin.stock_info as si
# import plot

# download data
with open('datasets/crypto_list.csv') as f :
    crypto_name = f.read().splitlines()
    for crypto in crypto_name:
        symbol = crypto.split()[0]
        print(symbol)
        data = get_data(symbol, start_date="01-01-2022",
                                end_date="08-14-2022",
                                index_as_date=True,
                                interval="1d"
                        )
        data.to_csv(f'datasets/daily_07-08/{symbol}.csv')




