import streamlit as st
import pandas as pd
from fyers_apiv3 import fyersModel
from datetime import datetime, timedelta
import fyers_login as log
import fyers_fun as fun
import pandas_ta as ta
import base64

# Mock user credentials (you can extend this for more users)
VALID_USERNAME = "admin"
VALID_PASSWORD = "password123"

# Function to load image and convert to base64
def load_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

# Function to set background image
def set_background(image_base64):
    page_bg_img = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{image_base64}");
        background-size: cover;
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Login function
def login():
    st.title("Stock Shooters")
    st.header("Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if username == VALID_USERNAME and password == VALID_PASSWORD:
            st.session_state['logged_in'] = True
            st.success("Logged in successfully!")
        else:
            st.error("Invalid username or password")

# Market predictor function
def market_predictor():
    st.title("Stock Shooters")  # Company name
    st.header("Market Range Predictor for NIFTYBANK")

    # User Input Section
    symbol = st.selectbox('Select the Symbol you want find out range ', options=["NSE:NIFTYBANK-INDEX","NSE:FINNIFTY-INDEX","BSE:BANKEX-INDEX","BSE:SENSEX-INDEX","NSE:NIFTY-INDEX"],index=None)
    timeframe = st.selectbox('Select Timeframe (in minutes)', options=["1", "3", "5", "15", "30", "60", "120"], index=None)

    # Variables
    client_id = "L012A42C9D-100"
    
    # Get access token (this function should return your token)
    access_token = log.get_token()

    # Initialize the FyersModel instance
    fyers = fyersModel.FyersModel(client_id=client_id, is_async=False, token=access_token, log_path="")

    # Fetch data from 10 days ago
    two_days_ago = datetime.now() - timedelta(days=10)
    from_date = str(two_days_ago.strftime("%Y-%m-%d"))
    to_date = str(datetime.now().strftime("%Y-%m-%d"))

    # Fetch live data when the user clicks the button
    if st.button('Predict Market Range'):
        # Get live data
        df = fun.live_data(symbol=symbol, timeframe=timeframe, from_date=from_date, to_date=to_date)

        # Calculate SMA (Simple Moving Average)
        df['SMA_20'] = ta.sma(df['close'], length=21)

        # Standard Deviation and Mean Calculation
        std_dev = df['SMA_20'].std()
        mean = df.iloc[-1]['SMA_20']
        upper_range = mean + std_dev
        lower_range = mean - std_dev

        # Display the ranges
        st.write(f"**Upper Range Value for {symbol} on {timeframe} min timeframe:** {upper_range:.2f}")
        st.write(f"**Lower Range Value for {symbol} on {timeframe} min timeframe:** {lower_range:.2f}")
    else:
        st.write("Click the button to predict the market range.")

# Main function
def main():
    # Set background image (optional)
    image_base64 = load_image("d:\youtube\stock shooter youtube\Stock Shooter logo 31.png")  # Use your own background image
    set_background(image_base64)

    # Check if user is logged in
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if not st.session_state['logged_in']:
        login()  # Show login page
    else:
        st.sidebar.button("Logout", on_click=lambda: logout())  # Show logout button in sidebar
        market_predictor()  # Show market prediction page after login

# Logout function
def logout():
    st.session_state['logged_in'] = False
    st.experimental_rerun()  # Force a rerun to go back to login page

if __name__ == '__main__':
    main()
