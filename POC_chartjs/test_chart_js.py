import csv

import pandas as pd
from
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

'''
d = {}
datafiles = os.listdir('dataset/daily')
for filesname in datafiles:
    df = pd.read_csv(f'dataset/daily/{filesname}')
    df.rename(columns={'Unnamed: 0': 'date'}, inplace=True)
    d[filesname] = df.columns

frame = pd.DataFrame.from_dict(d)
print(frame)
'''

df_main = pd.DataFrame()
datafiles = os.listdir('dataset/daily')
for filesname in datafiles:
    df = pd.read_csv(f'dataset/daily/{filesname}')
    df_main = df_main.concat(df.tail(5))
print(df_main)

@app.route("/")
def hello_world():
    ohlc_dict = {}



    return render_template('index_apexjs.html',tables=[df.to_html(classes='data')])






if __name__ == "__main__":
   app.run(host='0.0.0.0', port=5000, debug=True)#app.run(debug=True)