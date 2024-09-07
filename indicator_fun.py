from datetime import datetime,time
import pandas as pd 
import pandas_ta as ta
import time

def LTP(live_data):
    while 1:
        ltp=live_data.iloc[-1]
        ltp=ltp.iloc[3]
        return(ltp)
    
def rsi(live_data):
    
    # Calculate RSI using pandas_ta
    live_data["RSI"]=live_data.ta.rsi(length=14)

    
    return(live_data["RSI"]) 
def SMA(live_data,length):
    # Calculate 20-period simple moving average (SMA) using ta_pandas library
    live_data['SMA'] = ta.sma(live_data['close'], length=length)

    return(live_data["SMA"]) 
def bollinger_band(live_data):
     # Calculate 20-period simple moving average (SMA) using ta_pandas library
    live_data['sma_20'] = ta.sma(live_data['close'], length=20)

    # Calculate Bollinger Bands
    bollinger_multiplier = 2  # You can adjust this multiplier based on your preference
    live_data['upper_band'] = live_data['sma_20'] + (bollinger_multiplier * live_data['close'].rolling(window=20).std())
    live_data['lower_band'] = live_data['sma_20'] - (bollinger_multiplier * live_data['close'].rolling(window=20).std())
    #genarating buy signal when close is lower than lower_band
    live_data['buy_signal'] = 0
    live_data.loc[live_data['close'] < live_data['lower_band'], 'buy_signal'] = 1

    # Generate sell signal when close is greter than upper_band
    live_data['sell_signal'] = 0
    live_data.loc[live_data['close'] > live_data['upper_band'], 'sell_signal'] = 1

    # Print only sma_20, upper_band, lower_band values
    return (live_data[['buy_signal', 'sell_signal','sma_20']])
def EMA(live_data,length):
    # Calculate the 200-period EMA using pandas_ta
    live_data['ema'] = ta.ema(live_data['close'], length=length)
    
    return (live_data[['ema']]) 



def macd(live_data):

    macd=live_data.ta.macd(fast=12, slow=26, signal=9,append=True)
    return(macd)

#calculatre the ATR
def ATR(live_data):
    live_data['ATR'] = ta.atr(live_data['high'], live_data['low'], live_data['close'])
    a=live_data["ATR"]
    return(a)
    
# Calculate ADX indicator
def ADX(live_data):
    adx=live_data.ta.adx(append=1)
    return(adx)
def Vwap(live_data):
    live_data['vWAP'] = ta.vwap(high=live_data['high'], low=live_data['low'], close=live_data['close'], volume=live_data['tick_volume'])
    return live_data['vWAP']
# Calculate SuperTrend
def calculate_supertrend(df, period, multiplier):
    hl2 = (df['high'] + df['low']) / 2
    atr = ta.atr(df['high'], df['low'], df['close'], length=period)

    upperband = hl2 + (multiplier * atr)
    lowerband = hl2 - (multiplier * atr)

    trend = pd.Series(1, index=df.index)
    trend = trend.where(df['close'] <= lowerband, 0)
    trend = trend.where(df['close'] >= upperband, 1)
    trend = trend.shift(1)
    supertrend = (trend == 1) * lowerband + (trend == 0) * upperband
    return supertrend

#data['supertrend'] = calculate_supertrend(data, period=7, multiplier=2.5)

def calculate_stochastic_oscillator(df, fastk_period=14, slowk_period=3, slowd_period=3):
    
        stoch = ta.stoch(df['high'], df['low'], df['close'], fastk_period=fastk_period, slowk_period=slowk_period, slowd_period=slowd_period)
        return stoch
    
def fibonacci_retracement_uptrend(high, low):
    difference = high - low
    return {
        '23.6%': high - difference * 0.236,
        '38.2%': high - difference * 0.382,
        '50%': high - difference * 0.5,
        '61.8%': high - difference * 0.618,
        '100%': low
    }   

def fibonacci_retracement_downtrend(high, low):
    difference =  low-high
    return {
        '23.6%': low - difference * 0.236,
        '38.2%': low - difference * 0.382,
        '50%': low - difference * 0.5,
        '61.8%': low - difference * 0.618,
        '100%': high
    }   
def close(live_data):
    while 1:
        close=live_data.iloc[-2]
        close=close.iloc[3]
        return(close)


def calculate_heikin_ashi(df):
    close = (df['open'] + df['high'] + df['low'] + df['close']) / 4
    open = (df['open'].shift(1) + df['close'].shift(1)) / 2
    high = df[['high', 'open', 'close']].max(axis=1)
    low = df[['low', 'open', 'close']].min(axis=1)
    
    df['close'] = close
    df['cpen'] = open
    df['high'] = high
    df['low'] = low
    
    return df[['open', 'high', 'low', 'close']]
