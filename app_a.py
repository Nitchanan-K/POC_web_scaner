import csv
from flask import Flask, render_template, request
from patterns_list import candlestick_patterns
import talib
# import request and API data download
from yahoo_fin.stock_info import *
from yahoo_fin.stock_info import get_analysts_info
import yahoo_fin.stock_info as si
# os
import os

app = Flask(__name__)

@app.route("/")
def index():
    pattern = request.args.get('pattern', None)
    crypto_dict = {}

    with open('dataset/crypto_list.csv') as f:
        for row in csv.reader(f):
            crypto_dict[row[0]] = {'crypto': row[0].split('-')[0]}


    if pattern:
        datafiles = os.listdir('dataset/daily') # get lists of all CSV files
        for filename in datafiles:              # loop for each file
            df = pd.read_csv(f'dataset/daily/{filename}')
            df.rename(columns={'Unnamed: 0':'date'},inplace=True)
            pattern_function = getattr(talib,pattern) # getattr talib.pattern / pattern = select option input from web
            symbol = filename.split('.')[0]           # get symbol from filename

            try:
                # result is the dataset that returned after applied ta-lib candle pattern
                result = pattern_function(df['open'],df['high'],df['low'],df['close'])
                # last is the result lasttest value
                last = result.tail(1).values[0]
                #print(last)
                if last > 0:
                    crypto_dict[symbol][pattern] = 'bullish' # set pattern value to use

                elif last < 0 :
                    crypto_dict[symbol][pattern] = 'bearish'

                else:
                    crypto_dict[symbol][pattern] = None

            except:
                pass

    return render_template('index.html', candlestick_patterns=candlestick_patterns,crypto_dict=crypto_dict,pattern=pattern)


@app.route("/snapshot")
def snapshot():
    with open('dataset/crypto_list.csv') as f:
        crypto_name = f.read().splitlines()
        for crypto in crypto_name:
            symbol = crypto.split()[0]
            data = get_data(symbol, start_date="01-01-2022",
                            end_date="08-01-2022", index_as_date=True,
                            interval="1d")
            data.to_csv(f'dataset/daily/{symbol}.csv')


    return {
        'code': 'sucess'
    }

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=5000, debug=True)#app.run(debug=True)