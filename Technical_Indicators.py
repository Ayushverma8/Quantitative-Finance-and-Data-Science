# Purpose: Gather Data on equities in the technology sector
# Date: 5/11/2018

# Import required libraries
import datetime as dt
import os
import pandas as pd
import pandas_datareader.data as web

# Create dataframe for IT equities
equities_IT = pd.read_csv('data/StockSymbols_All.csv', header = None)
equities_IT.columns = ['Symbol', 'Name']
print(equities_IT.head())

# Create vector for IT equity sybols
symbols_IT = equities_IT['Symbol']
print(symbols_IT)

# Create directory for time series data
if not os.path.exists('data/equities_IT_TS'):
    os.makedirs('data/equities_IT_TS')
    
# Create directory for preprocessed time series data
if not os.path.exists('data/equities_IT_TS/preprocessed'):
    os.makedirs('data/equities_IT_TS/preprocessed')
    
# Create directory for processed time series data
if not os.path.exists('data/equities_IT_TS/processed'):
    os.makedirs('data/equities_IT_TS/processed')

# Function to calculate average volume over a specified interval of days
def calculate_avg_vol_for_interval(equity, days):
    equity['{}d Avg Vol'.format(days)] = equity['Volume'].rolling(window = days).mean()

# Function to calculate simple moving average over a specified interval of days    
def calculate_simple_moving_avg_for_interval(equity, days):
    equity['{}d SMA'.format(days)] = equity['Adj Close'].rolling(window = days).mean()
   
# Function to calculate exponential moving average over a specified interval of days
def calculate_exp_moving_avg_for_interval(equity, days):
    equity['{}d EMA'.format(days)] = equity['Adj Close'].ewm(span = days).mean()
    
# Function to calculate price low over specified interval of days
def calculate_price_low_for_interval(equity, days):
    equity['{}d Low'.format(days)] = equity['Adj Close'].rolling(window = days).min()
    
# Function to calculate price high over specified interval of days
def calculate_price_high_for_interval(equity, days):
    equity['{}d High'.format(days)] = equity['Adj Close'].rolling(window = days).max()

# Function to calculate per day price changes with columns for gain and loss
def calculate_per_day_price_change(equity):
    equity['Price Change'] = equity['Adj Close'].diff(periods = 1)
    equity['Gain'] = [x if x > 0 else 0 for x in equity['Price Change']]
    equity['Loss'] = [-x if x < 0 else 0 for x in equity['Price Change']]

# Function to calculate average gain over specified interval of days
def calculate_avg_gain_for_interval(equity, days):
    equity['{}d Avg Gain'.format(days)] = equity['Gain'].rolling(window = days).sum() / days
    
# Function to calculate average loss over specified interval of days
def calculate_avg_loss_for_interval(equity, days):
    equity['{}d Avg Loss'.format(days)] = equity['Loss'].rolling(window = days).sum() / days
    
# Function to calculate RSI for specified interval of days
def calculate_rsi(equity, days):
    calculate_avg_gain_for_interval(equity, days)
    calculate_avg_loss_for_interval(equity, days)
    equity['{}d RSI'.format(days)] = 100 - (100 / (1 + (equity['{}d Avg Gain'.format(days)] / equity['{}d Avg Loss'.format(days)])))
    
# Function to calculate MACD, MACD Signal Line, and MACD Histogram for specified short, long, and signal parameters
def calculate_macd(equity, short, long, signal):
    calculate_exp_moving_avg_for_interval(equity, short)
    calculate_exp_moving_avg_for_interval(equity, long)
    equity['MACD {} {} {}'.format(short, long, signal)] = equity['{}d EMA'.format(short)] - equity['{}d EMA'.format(long)]
    equity['MACD {} {} {} Signal'.format(short, long, signal)] = equity['MACD {} {} {}'.format(short, long, signal)].ewm(span = signal).mean()
    equity['MACD {} {} {} Hist'.format(short, long, signal)] = equity['MACD {} {} {}'.format(short, long, signal)] - equity['MACD {} {} {} Signal'.format(short, long, signal)]
    
# Function to calculate average rate of change for a particular column over a specified interval of days
def calculate_avg_roc_for_interval(equity, column, days):
    equity['{} {}d Avg ROC'.format(column, days)] = (equity[column] - equity[column].shift(days)) / days
    
# Function to calculate Accumulation Distribution Line (ADL)
def calculate_adl(equity):
    mfl = ((equity['Close'] - equity['Low']) - (equity['High'] - equity['Close'])) / (equity['High'] - equity['Low'])
    mfv = mfl * equity['Volume']
    equity['MFV'] = mfv
    equity['ADL'] = equity['MFV'].cumsum()

# Function to calculate Full Stochastics
def calculate_full_stochs(equity, periods, s1, s2):
    equity['%K'] = (equity['Close'] - equity['Low'].rolling(window = periods).min()) / (equity['High'].rolling(window = periods).max() - equity['Low'].rolling(window = periods).min()) * 100
    equity['%K Full'] = equity['%K'].rolling(window = s1).mean()
    equity['%D Full'] = equity['%K Full'].rolling(window = s2).mean()
    
# Function to calculate Chaikin Oscillator
def calculate_chaikin_osc(equity):
    equity['Chaikin'] = equity['ADL'].ewm(span = 3).mean() - equity['ADL'].ewm(span = 10).mean()
    
# Function to calculate technical indicators for an equity
def calculate_indicators_for_equity(equity):
    calculate_avg_vol_for_interval(equity, 5)
    calculate_avg_vol_for_interval(equity, 30)
    
    calculate_simple_moving_avg_for_interval(equity, 15)
    calculate_simple_moving_avg_for_interval(equity, 60)
    calculate_simple_moving_avg_for_interval(equity, 100)
    
    calculate_exp_moving_avg_for_interval(equity, 10)
    calculate_exp_moving_avg_for_interval(equity, 15)
    calculate_exp_moving_avg_for_interval(equity, 30)
    calculate_exp_moving_avg_for_interval(equity, 45)
    
    calculate_macd(equity, 12, 26, 9)

    equity['5d Avg Vol vs 30d Avg Vol'] = equity['5d Avg Vol'] / equity['30d Avg Vol']
    
    calculate_price_low_for_interval(equity, 30)
    calculate_price_high_for_interval(equity, 30)
    calculate_price_low_for_interval(equity, 200)
    calculate_price_high_for_interval(equity, 200)
    
    calculate_per_day_price_change(equity)
    
    calculate_rsi(equity, 14)
    
    calculate_full_stochs(equity, 14, 3, 3)
    
    calculate_adl(equity)
    
    calculate_chaikin_osc(equity)
    
# Define function to calculate response and create column for target label
def calculate_target_label_for_interval(equity, days, threshold):
    equity['{}d Pct Change'.format(days)] = (equity['Adj Close'].shift(-days) - equity['Adj Close']) / equity['Adj Close']
    equity['{}d Label'.format(days)] = [1 if x > threshold else -1 if x < -threshold else 0 for x in equity['{}d Pct Change'.format(days)]]

# Window of time to grab equity data
start = dt.datetime(1977, 1, 1)
end = dt.datetime(2017, 7, 31)

# Collect time series data for all possible symbols and store it locally so it does not have to be re-pulled from yahoo
for symbol in symbols_IT:
    if not os.path.exists('data/equities_IT_TS/preprocessed/{}.csv'.format(symbol)):
        try:
            df = web.DataReader(symbol, 'yahoo', start, end)
            df.to_csv('data/equities_IT_TS/preprocessed/{}.csv'.format(symbol))
        except:
            print(symbol)

# For each symbol, look for file of time series data in preprocessed directory
# If exists, retrieve the data, calculate technical indicators and response label
# Store updated data into the processed directory
for symbol in symbols_IT:
    if os.path.exists('data/equities_IT_TS/preprocessed/{}.csv'.format(symbol)):
        df = pd.read_csv('data/equities_IT_TS/preprocessed/{}.csv'.format(symbol))
        calculate_indicators_for_equity(df)
        calculate_target_label_for_interval(df, 15, .1)
        df.to_csv('data/equities_IT_TS/processed/{}.csv'.format(symbol))
