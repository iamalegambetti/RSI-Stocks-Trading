import pandas as pd
import numpy as np

data = 'russel.csv'
#loading data at 13/09/2019, the data is yearly
df = pd.read_csv(data, index_col = 0)
df = df.drop(['Open', 'High', 'Low', 'Adj Close', 'Volume'], axis = 1)

df = df.iloc[::-1] #reversing thte dataframe

def twenty_days_ma(df, col):

    """
    Computes the 20 days moving average for a specific column in a DataFrame
    """

    averages = []
    stds = []
    indices = []

    for i in range(0, len(df[col]) - 20):

        idx = df[col][i:i+1].index[0]
        temp = df[col][i:i+20]
        average = temp.mean()
        std = temp.std()

        averages.append(average)
        stds.append(std)
        indices.append(idx)

    data = {'Averages':averages, 'StDevs': stds}
    df_local = pd.DataFrame(data, index = indices)

    return df_local


def mean(nums):
    total = 0
    for num in nums:
        total += num
    res = total / len(nums)
    return res


def rsi(df, col, days = 20):
    """Computes the RSI for a specific column in a Dataframe"""

    rsis = []
    indices = []

    for i in range(0, len(df[col]) - days):

        ups = []
        down = []

        idx = df[col][i:i+1].index[0] #index
        temp = df[col][i:i+days] #selected dataframe portion

        for el in temp.pct_change():
            #print(el)
            if el < 0:
                down.append(el)
            else:
                ups.append(el)

        ups = ups[1:]
        down = down[1:]
        down = [(-i) for i in down] #converting to positives

        #print('Ups',ups)
        #print('Downs',down)

        #computing average high and low
        if len(ups) >= 1:
            gain = mean(ups) #average percentage change in high
        else:
            gain = 0.000001
        print('Gain', gain)

        if len(down) >=1:
            loss = mean(down) #average percentage change in low
        else:
            loss = 0.000001

        print('Loss', loss)

        #computing single rsi
        ratio_gain_loss_plus_one = 1 + gain/loss
        ratio_one_hudred = 100 / ratio_gain_loss_plus_one
        rsi = 100 - ratio_one_hudred

        #print(rsi)

        #appending results
        rsis.append(rsi)
        indices.append(idx)

    #building dataframe
    data = {'RSI': rsis}
    df_local = pd.DataFrame(data, index = indices)

    return df_local


# CREATING DATAFRAME WITH AVERAGES AND STANDARD DEVIATIONS BANDS
band_width = 2
df_av_std = twenty_days_ma(df, 'Close') #dataframe of averages and stds
df_av_std['UpperBand'] = df_av_std['Averages'] + band_width * df_av_std['StDevs']
df_av_std['LowerBand'] = df_av_std['Averages'] - band_width * df_av_std['StDevs']
df_av_std = df_av_std.iloc[::-1] #reversing thte dataframe again

# CREATING THE DATAFRAME OF RSI
rsi = rsi(df, 'Close')
rsi = rsi.iloc[::-1]

# CONCATENATING DATAFRAMES OF AVERAGES, CLOSE AND RSI
new_df = pd.concat([df_av_std, rsi, df['Close']], axis = 1)
df = new_df.dropna()

# EXPORT TO CSV FOR EACH DIFFERENT CASE
if data == 'russell2000_5years.csv':
    df.to_csv('russell2000_5years_average_rsi.csv', sep = ';')
elif data == 'russel.csv':
    df.to_csv('russell2000_1year_average_rsi.csv', sep = ';')
elif data == 'sp500_5_years.csv':
    df.to_csv('sp500_5_years_average_rsi.csv', sep = ';')
else:
    pass


# SOME VISUALUZATION
import matplotlib.pyplot as plt
plt.figure(figsize = (10, 6))
plt.plot(df['Averages'], lw = 2, c = 'blue', label = 'Average')
plt.plot(df['UpperBand'], lw = 1.6, c = 'red', label = 'Upper Bound')
plt.plot(df['LowerBand'], lw = 1.6, c = 'red', label = 'Lower Bound')
plt.plot(df['Close'], lw = 1.6, c = 'green', label = 'Close Price')
plt.xticks(range(0, len(df_av_std)))
plt.title('Russel 2000 20-days Moving Average', fontsize = 36)
plt.legend()

rsi.plot(figsize = (10, 6), lw = 1.8)
plt.plot(y = 30)
plt.title('RSI', fontsize = 36)

plt.show()
