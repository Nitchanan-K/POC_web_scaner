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

    if symbol in symbols:
        print(df)
        eth_df = df

candlestick = go.Candlestick(x=eth_df['date'],open=eth_df['open'],high=eth_df['high'],low=eth_df['low'],close=eth_df['close'])
upper_band = go.Scatter(x=eth_df['date'],y=eth_df['upper_band'], name='Upper Bollinger Band', line={'color':'red'})
lower_band = go.Scatter(x=eth_df['date'],y=eth_df['lower_band'], name='Lower Bollinger Band', line={'color':'red'})



fig = go.Figure(data=[candlestick,upper_band,lower_band])

fig.layout.xaxis.type = 'category'
fig.layout.xaxis.rangeslider.visible = False
fig.show()