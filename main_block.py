import pandas as pd
import pandas_ta as ta
import time
import os
from binance.um_futures import UMFutures
from binance.error import ClientError
from dotenv import load_dotenv

# Set global variables
'''
api_key = 'GEcw0dAon6Rg52SQkGc1jwtHQdA8rjpUw0ZoTQ8hvTHbCABfz6gnfCmrEjpA1rV3'
api_secret = 'rAGySyby1PYddQNaQqxGQozFK0dx2Y5xSa3ITN7cUF2qxQBR4o62fr1sQm8dWJK7'
'''

# Load environment variables from .env file
load_dotenv()
# Access the Binance API keys
API_KEY = os.getenv("BINANCE_API_KEY")
SECRET_KEY = os.getenv("BINANCE_SECRET_KEY")

# Sample check to confirm variables loaded correctly
if not API_KEY or not SECRET_KEY:
    raise ValueError("API keys not found. Please set them in the environment or .env file.")

client = UMFutures(API_KEY, SECRET_KEY)

TSL = 0.01
volume = 5  # USDT
leverage = 5
type = 'ISOLATED'

symbol = 'BTCUSDT'


'''
import requests

def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        response.raise_for_status()  # Check if request was successful
        ip = response.json().get('ip')
        return ip
    except requests.RequestException as e:
        print(f"Error fetching IP address: {e}")
        return None

# Usage
my_ip = get_public_ip()
if my_ip:
    print("Your public IP address is:", my_ip)
else:
    print("Could not retrieve IP address.")
'''


# 1. GET_ACCOUNT_BALANCE function
def GET_ACCOUNT_BALANCE():
    try:
        balance_info = client.balance()
        for balance in balance_info:
            if balance['asset'] == 'USDT':
                print(f"Remaining USDT Balance: {balance['balance']}")
    except ClientError as e:
        print(f"Error fetching account balance: {e}")


# 2. EMA_CALCULATOR function
def EMA_CALCULATOR(df, length):
    df['hl2'] = (df['high'] + df['low']) / 2
    return ta.ema(df['hl2'].astype(float), length=length)


# 3. DATA_FETCHER function
def DATA_FETCHER():
    try:
        candles = client.klines(symbol=symbol, interval='1m', limit=40)
        df = pd.DataFrame(candles, columns=['time', 'open', 'high', 'low', 'close', 'volume', 
                                            'close_time', 'quote_asset_volume', 'num_trades',
                                            'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
        df['open'] = df['open'].astype(float)
        df['high'] = df['high'].astype(float)
        df['low'] = df['low'].astype(float)
        df['close'] = df['close'].astype(float)
        df['ema_5'] = EMA_CALCULATOR(df, 5)
        df['ema_34'] = EMA_CALCULATOR(df, 34)
        return df
    except ClientError as e:
        print(f"Error fetching data: {e}")
        return None


# 4. SET_LEVERAGE function
def SET_LEVERAGE():
    try:
        client.change_leverage(symbol=symbol, leverage=leverage)
        print(f"Leverage set to {leverage}x for {symbol}")
    except ClientError as e:
        print(f"Error setting leverage: {e}")


# 5. SET_MARGIN_TYPE function
def SET_MARGIN_TYPE():
    try:
        client.change_margin_type(symbol=symbol, marginType=type)
        print(f"Margin type set to {type} for {symbol}")
    except ClientError as e:
        print(f"Error setting margin type: {e}")


# 6. GET_PRICE_PRECISION function
def GET_PRICE_PRECISION():
    try:
        symbol_info = client.exchange_info(symbol=symbol)
        return symbol_info['symbols'][0]['pricePrecision']
    except ClientError as e:
        print(f"Error getting price precision: {e}")


# 7. GET_QUANTITY_PRECISION function
def GET_QUANTITY_PRECISION():
    try:
        symbol_info = client.exchange_info(symbol=symbol)
        return symbol_info['symbols'][0]['quantityPrecision']
    except ClientError as e:
        print(f"Error getting quantity precision: {e}")


# 8. OPEN_ORDER function
def OPEN_ORDER(side, qty):
    try:
        price_precision = GET_PRICE_PRECISION()
        quantity_precision = GET_QUANTITY_PRECISION()
        price = float(client.mark_price(symbol=symbol)['markPrice'])
        price = round(price, price_precision)
        qty = round(qty, quantity_precision)
        
        if side == 'BUY':
            order = client.new_order(symbol=symbol, side='BUY', type='LIMIT', price=price, quantity=qty, timeInForce='GTC')
        elif side == 'SELL':
            order = client.new_order(symbol=symbol, side='SELL', type='LIMIT', price=price, quantity=qty, timeInForce='GTC')
        
        print(f"Order placed: {order}")
    except ClientError as e:
        print(f"Error placing order: {e}")


# 9. CHECK_POSITIONS function
def CHECK_POSITIONS():
    try:
        positions = client.position_information(symbol=symbol)
        for position in positions:
            if float(position['positionAmt']) != 0:
                print(f"Open position: {position}")
                return position
        return None
    except ClientError as e:
        print(f"Error checking positions: {e}")


# 10. CLOSE_OPEN_ORDER function
def CLOSE_OPEN_ORDER():
    try:
        open_orders = client.get_open_orders(symbol=symbol)
        if open_orders:
            for order in open_orders:
                result = client.cancel_order(symbol=symbol, orderId=order['orderId'])
                print(f"Closed open order: {result}")
    except ClientError as e:
        print(f"Error closing open orders: {e}")


# 11. TRADING_ALGO function
def TRADING_ALGO(df):
    if df['ema_5'].iloc[-1] > df['ema_34'].iloc[-1]:
        print("Long entry condition met!")
        OPEN_ORDER('BUY', volume)
    elif df['ema_34'].iloc[-1] > df['ema_5'].iloc[-1]:
        print("Short entry condition met!")
        OPEN_ORDER('SELL', volume)
    else:
        print("No trading condition met")

# Main loop
if __name__ == "__main__":
    # Set leverage and margin type
    SET_LEVERAGE()
    SET_MARGIN_TYPE()
    
    # Check for any open positions and close them if any
    position = CHECK_POSITIONS()
    if position:
        CLOSE_OPEN_ORDER()
    
    while True:
        # Fetch new data
        df = DATA_FETCHER()
        print (df)
        
        if df is not None:
            # Get account balance
            GET_ACCOUNT_BALANCE()

            # Execute trading logic
            #################################TRADING_ALGO(df)

        # Wait for 60 seconds before fetching data again
        time.sleep(60)

'''




import traceback

try:
    result = 10 / 0
except Exception as e:
    tb = traceback.extract_tb(e.__traceback__)
    line_number = tb[-1].lineno
    
    with open("error_log.txt", "w") as f:
        f.write(f"Error occurred on line: {line_number}")
        f.write('\n')
        f.write(f"An error occurred: {e}")
        f.write('\n\n')
        traceback.print_exc(file=f)

'''