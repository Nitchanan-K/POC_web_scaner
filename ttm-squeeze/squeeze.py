import  os,pandas
# improt plot
import  plotly.graph_objects as go

symbols = ['symbol']

for filename in os.listdir('datasets/daily_07-08'):
    symbol = filename.split("-")[0]
    print(symbol)
    df = pandas.read_csv(f'datasets/daily_07-08/{filename}')
    df.rename(columns={'Unnamed: 0': 'date'}, inplace=True)

    if df.empty:
        continue

    # cal 20 sma
    df['20sma'] = df['close'].rolling(window=20).mean()

    # make bb band
    # std dev
    df['stddev'] = df['close'].rolling(window=20).std()
    # lower band / upper band
    df['lower_band'] = df['20sma'] - (2 * df['stddev'])
    df['upper_band'] = df['20sma'] + (2 * df['stddev'])

    # Cal Ture range
    df['TR'] = abs(df['high'] - df['low'])
    df['ATR'] = df['TR'].rolling(window=20).mean()

    # make colum of  upper_keltner / lower_keltner
    df['lower_keltner'] = df['20sma'] - (df['ATR'] * 1.5)
    df['upper_keltner'] = df['20sma'] + (df['ATR'] * 1.5)

    def in_squeeze(df):
        return df['lower_band'] > df['lower_keltner'] and df['upper_band'] < df['upper_keltner']

    df['squeeze_on'] = df.apply(in_squeeze, axis=1)

    # find day in past that squeeze_on and not in last day [-3] 3 days ago
    if df.iloc[-3]['squeeze_on'] and not df.iloc[-1]['squeeze_on']:
        print(f"{symbol} is coming out the squeeze ")

    # check for recent day squeeze
    #if df.iloc[-1]['squeeze_on']:
        #print(f"{symbol} is in the squeeze!!!")


    if symbol == "DOGE":
        print(df)
        symbol_df = df



# Define plot
candlestick = go.Candlestick(x=symbol_df['date'],open=symbol_df['open'],high=symbol_df['high'],low=symbol_df['low'],close=symbol_df['close'])
upper_band = go.Scatter(x=symbol_df['date'],y=symbol_df['upper_band'], name='Upper Bollinger Band', line={'color':'red'})
lower_band = go.Scatter(x=symbol_df['date'],y=symbol_df['lower_band'], name='Lower Bollinger Band', line={'color':'red'})
upper_keltner = go.Scatter(x=symbol_df['date'],y=symbol_df['upper_keltner'], name='Upper Keltner Channel', line={'color':'blue'})
lower_keltner = go.Scatter(x=symbol_df['date'],y=symbol_df['lower_keltner'], name='Lower Keltner Channel', line={'color':'blue'})





fig = go.Figure(data=[candlestick,upper_band,lower_band,upper_keltner,lower_keltner])

fig.layout.xaxis.type = 'category'
fig.layout.xaxis.rangeslider.visible = False
fig.show()
