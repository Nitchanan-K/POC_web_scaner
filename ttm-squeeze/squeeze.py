import  os,pandas
# improt plot
import  plotly.graph_objects as go

symbols = ['ETH']

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

    # Ture range
    df['TR'] = abs(df['high'] - df['low'])
    df['ATR'] = df['TR'].rolling(window=20).mean()

    df['lower_keltner'] = df['20sma'] - (df['ATR'] * 1.5)
    df['upper_keltner'] = df['20sma'] + (df['ATR'] * 1.5)

    def in_squeeze(df):
        return df['lower_band'] > df['lower_keltner'] and df['upper_band'] < df['upper_keltner']

    df['squeeze_on'] = df.apply(in_squeeze, axis=1)

    if df.iloc[-1]['squeeze_on']:
        print(f"{symbol} is in the squeeze!!!")

    if symbol == "KSM":
        print(df)
        eth_df = df



# Define plot
candlestick = go.Candlestick(x=eth_df['date'],open=eth_df['open'],high=eth_df['high'],low=eth_df['low'],close=eth_df['close'])
upper_band = go.Scatter(x=eth_df['date'],y=eth_df['upper_band'], name='Upper Bollinger Band', line={'color':'red'})
lower_band = go.Scatter(x=eth_df['date'],y=eth_df['lower_band'], name='Lower Bollinger Band', line={'color':'red'})
upper_keltner = go.Scatter(x=eth_df['date'],y=eth_df['upper_keltner'], name='Upper Keltner Channel', line={'color':'blue'})
lower_keltner = go.Scatter(x=eth_df['date'],y=eth_df['lower_keltner'], name='Lower Keltner Channel', line={'color':'blue'})





fig = go.Figure(data=[candlestick,upper_band,lower_band,upper_keltner,lower_keltner])

fig.layout.xaxis.type = 'category'
fig.layout.xaxis.rangeslider.visible = False
fig.show()
