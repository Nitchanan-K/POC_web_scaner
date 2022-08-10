import csv

import pandas as pd
from pandas import concat
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



@app.route("/")
def hello_world():
    df_main = pd.DataFrame()
    datafiles = os.listdir('dataset/daily')
    for filesname in datafiles:
        df = pd.read_csv(f'dataset/daily/{filesname}')
        df.rename(columns={'Unnamed: 0': 'date'}, inplace=True)
        df_main = pd.concat([df_main,df.tail(5)])
        df_main.reset_index(drop=True,inplace=True)
        '''
        df_main = df_main.append(df.tail(5))
        df_main
        df_main.reset_index(drop=True, inplace=True)
        '''
    #print(df_main)
    print(df_main)

    return render_template('index_apexjs.html',df_main=df_main)






if __name__ == "__main__":
   app.run(host='0.0.0.0', port=5000, debug=True)#app.run(debug=True)