import fyers_login as log
import pandas as pd
from fyers_apiv3 import fyersModel
from datetime import datetime, timedelta,date,time
import fyers_fun as fun
import indicator_fun as ifun
import pandas_ta as ta
import time
from datetime import datetime
symbol="NSE:NIFTYBANK-INDEX"
timeframe="30"
client_id = "L012A42C9D-100"
access_token=log.get_token()
# Initialize the FyersModel instance with your client_id, access_token, and enable async mode
fyers = fyersModel.FyersModel(client_id=client_id, is_async=False, token=access_token, log_path="")
two_days_ago = datetime.now() - timedelta(days=10)
from_date = str(two_days_ago.strftime("%Y-%m-%d"))
to_date =str(datetime.now().strftime("%Y-%m-%d"))
df=fun.live_data(symbol=symbol,timeframe=timeframe,from_date=from_date,to_date=to_date)
df['SMA_20'] = ta.sma(df['close'], length=21)
# selected_column = df['SMA_20']
std_dev = df['SMA_20'].std()
mean=df.iloc[-1]
mean=mean.iloc[-1]
upper_range=mean+std_dev
lower_range=mean-std_dev


