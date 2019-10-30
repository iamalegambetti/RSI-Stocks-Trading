import pandas as pd

#loading data
df = pd.read_csv('russell2000_1year_average_rsi.csv', sep = ';', index_col=0)

"""
The strategy works in this way: We open a long position when there’s a close
outside the lower band with the RSI in oversold territory, hence below 30; while
for short position, we short it when the close is above the upper band and the
RSI is overbought, above 70.
"""

# COLUMNS
#['Averages', 'StDevs', 'UpperBand', 'LowerBand', 'RSI', 'Close']

# CREATING THE MODEL
def model(df, endowment, rsi_buy, rsi_sell):

    #INITIALIZING ECONOMIC VALUES
    total_sold = 0 #Cumulative Stake Sold
    n_investments = 0 #Number of Investments Made
    in_market_stake = 0 #Current Stake In The Market

    # CREATE A COLUMN FOR THE DAILY RETURNS
    df['Returns'] = df['Close'].pct_change()
    df = df.dropna()

    # CREATING A COUNTER TO DEAL WITH THE LAST ITERATION
    last_iteration = len(df.index)
    count = 0

    for idx in df.index:

        count += 1 #Refresh the counter

        # BUY STATEMENT
        if df['Close'].loc[idx] < df['LowerBand'].loc[idx] and df['RSI'].loc[idx] <= rsi_buy:
            print('Buying!')
            in_market_stake += endowment
            n_investments += 1 #count the number of investments
            continue

        # SELL STATEMENT
        if df['Close'].loc[idx] > df['UpperBand'].loc[idx] and df['RSI'].loc[idx] >= rsi_sell:
            print('Selling!')
            total_sold += in_market_stake
            in_market_stake = 0
            continue

        # COMPUTE the RETURN of the investment fund DAY-BY-DAY
        in_market_stake = in_market_stake * (1 + df['Returns'].loc[idx])
        print(f'Current Stake in the Market is {in_market_stake}')

        # HANDLING LAST ITERATION -> Transfer everything to total sold
        if count == last_iteration:
            total_sold += in_market_stake
            in_market_stake = 0

    # BRUTE FORCE RETURN FORMULA; NOT 100% CORRECT TO SYMPLIFY
    numerator = (total_sold - n_investments * endowment)
    denominator = n_investments * endowment
    total_return = numerator / denominator
    print('\n')
    #to edit!
    return f'Total Return Earned {100 * round(total_return, 4)} %'


#MODEL OUTPUT
rsi_buy = 30
rsi_sell = 70
mod = model(df, 100, rsi_buy, rsi_sell) #df, endowment
print(mod)

# TO FIX:
# 1. Not convicing me the RSI COMPUTATOR
# 2. Fix the Return Formula
