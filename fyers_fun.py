import fyers_login as log
import pandas as pd
from fyers_apiv3 import fyersModel
from datetime import datetime, timedelta,date,time

token=log.get_token()
client_id = "L012A42C9D-100"
access_token = token
# Initialize the FyersModel instance with your client_id, access_token, and enable async mode
fyers = fyersModel.FyersModel(client_id=client_id, is_async=False, token=access_token, log_path="")
def live_data(symbol,timeframe,from_date,to_date,fyers=fyers):
    
    data = {
    "symbol":symbol,
    "resolution":timeframe,
    "date_format":"1",
    "range_from":from_date,
    "range_to":to_date,
    "cont_flag":"1"
    }
    
    df= pd.DataFrame(fyers.history(data=data)["candles"])
    df.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
    df['date'] = pd.to_datetime(pd.to_numeric(df['date']), unit='s')
    df.set_index('date', inplace=True)
    return df

#total available balances
def balance(fyers=fyers):
    balances=fyers.funds()
    balances=balances['fund_limit'][-1]['equityAmount']
    return(balances)
#total pnl of all position
def pl_total(fyers=fyers):
    pl_total = fyers.positions()
    pl_total=pl_total['overall']['pl_total']
    return(pl_total)
#to identify total opean position 
def position(fyers=fyers):
    total_opean = fyers.positions()
    total_opean=total_opean['overall']['count_open']
    return(total_opean)
#to placing buy order
def buy_order(symbol,lot_size,fyers=fyers):

    data = {
    "symbol":symbol,
    "qty":lot_size,
    "type":2,
    "side":1,
    "productType":"INTRADAY",
    "limitPrice":0.0,
    "stopLoss":0.0,
    "validity":"DAY",
    "disclosedQty":0,
    "offlineOrder":False
    }
    response = fyers.place_order(data=data)
    return(response)
#to placing sell order 
def sell_order(symbol,lot_size,fyers=fyers):

    data = {
    "symbol":symbol,
    "qty":lot_size,
    "type":2,
    "side":-1,
    "productType":"INTRADAY",
    "limitPrice":0.0,
    "stopLoss":0.0,
    "validity":"DAY",
    "disclosedQty":0,
    "offlineOrder":False
    }
    response = fyers.place_order(data=data)
    return(response)


def close_position(fyers=fyers):
    data = {}
    response = fyers.exit_positions(data=data)
    return response

# Function to calculate risk per trade based on account balance and risk percentage
def risk_per_trade(riskt, balance=balance()):
    risk_per_trade = balance * riskt / 100
    return int(risk_per_trade)

# Function to calculate stop loss based on risk percentage and stop loss percentage
def sl(riskt, slp, ltp, balance=balance()):
    # Calculate risk per trade as 1% of account balance
    risk_per_trade = balance * riskt / 100
    # Calculate stop loss (SL) as 0.02% of bid price of symbol
    sl = ltp * slp / 100
    sl=round(sl / 0.05) * 0.05
    sl=round(sl,2)
    return sl
# Function to calculate lot size based on risk percentage, stop loss percentage, and last traded price
def calculate_lot_size(riskt, slp, ltp, balance=balance()):
    risk_per_trade = balance * riskt / 100
    # Calculate stop loss (SL) as 0.02% of bid price of symbol
    sl = ltp * slp / 100
    lot_sizes = int(risk_per_trade) / sl
    return int(lot_sizes)

# Function to check if it's trading time
def time_check():
    current_time = datetime.now().time()
    start_time = time(9,20)
    end_time = time(15,10)
    current_datetime = datetime.now()
    current_weekday = current_datetime.weekday()
    
    if 0 <= current_weekday <= 4 and start_time <= current_time <= end_time:
        return 1
    else:
        return 0

# Function to check if it's time to square off positions
def squre_off():
    current_time = datetime.now().strftime("%H:%M")
    squre_position = '15:15'  # Assuming squaring off at 3:15 PM
    if current_time > squre_position:
        return 1  # Time to square off
    if time_check():
        return 0  # Not time to square off yet


def o_position(symbol):
    lengh=fyers.positions()
    a=lengh['netPositions']
    a=(len(a))
    b=0
    while (a)>b:
        symbol=symbol
        id=lengh['netPositions'][b][ 'symbol']
        b=b+1
        if symbol==symbol:
            i=b-1
            netquntity=fyers.positions()
            netquntity=netquntity['netPositions'][i]['netQty' ]
            return(netquntity)

def o_pl_total(symbol):
    lengh=fyers.positions()
    a=lengh['netPositions']
    a=(len(a))
    b=0
    while (a)>b:
        symbol=symbol
        symbol=lengh['netPositions'][b][ 'symbol']
        b=b+1
        if symbol==symbol:
            i=b-1
            pnl=fyers.positions()
            pnl=pnl['netPositions'][i]['pl' ]
            return(pnl)
def SL_buy_order(symbol,lot_size,sl,ltp,fyers=fyers):

    data = {
    "symbol":symbol,
    "qty":lot_size,
    "type":3,
    "side":1,
    "productType":"INTRADAY",
    "limitPrice":0.0,
    "stopPrice":ltp+float(sl),
    "validity":"DAY",
    "disclosedQty":0,
    "offlineOrder":False
    }
    response = fyers.place_order(data=data)
    return(response)
#to placing sell order 
def SL_sell_order(symbol,lot_size,sl,ltp,fyers=fyers):

    data = {
    "symbol":symbol,
    "qty":lot_size,
    "type":3,
    "side":-1,
    "productType":"INTRADAY",
    "limitPrice":0.0,
    "stopPrice":ltp-float(sl),
    "validity":"DAY",
    "disclosedQty":0,
    "offlineOrder":False
    }
    response = fyers.place_order(data=data)
    return(response)
def cancel_order(id):
    data = {"id":id}
    response = fyers.cancel_order(data=data)
    return(response)
