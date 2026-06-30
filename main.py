import pandas as pd
import pandas_ta as ta
import time
from pytz import utc
import os
from binance.um_futures import UMFutures
from binance.error import ClientError
from dotenv import load_dotenv
from flask import Flask, render_template
from apscheduler.schedulers.background import BackgroundScheduler
import requests

# pip install python-dotenv

binance_btcusdt_futures_app = Flask(__name__)
a = 0

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
        positions = client.get_position_risk(symbol=symbol)
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









def SCHEDULED_TASK():
    # Check for any open positions and close them if any
    position = CHECK_POSITIONS()
    if position:
        CLOSE_OPEN_ORDER()
    
    #while True:
    # Fetch new data
    df = DATA_FETCHER()
    print (df[:5])
    
    if df is not None:
        # Get account balance
        GET_ACCOUNT_BALANCE()

        # Execute trading logic
        #################################TRADING_ALGO(df)

    # Wait for 60 seconds before fetching data again
    #time.sleep(60)


scheduler = BackgroundScheduler(timezone=utc)
scheduler.add_job(SCHEDULED_TASK, 'interval', minutes=1)

@binance_btcusdt_futures_app.route('/')
def HOME_PAGE():
    # Set leverage and margin type
    #################################SET_LEVERAGE()
    #################################SET_MARGIN_TYPE()
    global a
    
    if a==0:
        SCHEDULED_TASK()
        scheduler.start()
    a+=1
    
    '''
    54.254.162.138
    54.254.162.138
    '''
    
    
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
        print("YOUR PUBLIC IP ADDRESS IS :", my_ip)
    else:
        print("Could not retrieve IP address.")
    
    return render_template('homepage.html', message='<h1>balance fetched</h1>')
    
# Main loop
if __name__ == "__main__":
    
    try:
        binance_btcusdt_futures_app.run(host='0.0.0.0', port=5000)
    except (KeyboardInterrupt, SystemExit):
        print ('SOME ERROR HAS OCCURED IN THE ================= binance_btcusdt_futures_app')
        scheduler.shutdown()
