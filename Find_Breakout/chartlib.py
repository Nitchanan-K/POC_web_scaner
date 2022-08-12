import  os
import pandas as pd


# make function to check consolidating
def is_consolidating(df, percentage = float(2)):
    recent_candlesticks = df[-15:]
    #print(recent_candlesticks)

    max_close = recent_candlesticks['close'].max()
    min_close = recent_candlesticks['close'].min()

    # check %
    threshold = 1-(percentage / 100)
    if min_close > (max_close * threshold):
        return True

    return False
    #print(f" The max close was {max_close} and the min close was {min_close}")


# make function to check breaking out
def is_breaking_out(df, percentage = float(2.5)):
    last_close = df[-1:]['close'].values[0]

    # df[:-1] all but exclude last one
    if is_consolidating(df[:-1], percentage= percentage):
        recent_closes = df[-16:-1]

        # last close > 15 recent closes
        if last_close > recent_closes['close'].max():
            return True

    return False


# make data frame open file
# run functions
for filename in os.listdir('dataset/daily'):
    df = pd.read_csv(f'dataset/daily/{filename}')
    df.rename(columns={'Unnamed: 0': 'date'}, inplace=True)


    if is_consolidating(df,percentage=4):
        print(f"{filename} is consolidating")   # last 15 candles is consolidating between 2%


    if is_breaking_out(df):
        print(f"{filename} is Breaking Out")
