BTCUSDT Binance Futures Trading Bot
Overview

This project is a Python-based Binance USDT-M Futures trading bot designed to automate cryptocurrency trading using a simple EMA crossover strategy.

The bot connects directly to the Binance Futures API, retrieves live BTCUSDT market data every minute, calculates technical indicators, monitors account information, and places buy or sell orders automatically whenever trading conditions are satisfied.

The application has been written in a modular way where every trading operation is separated into individual functions, making the code easy to understand and extend.

Features
Binance Futures Integration

The bot uses the official Binance USDT Futures Python SDK to communicate with Binance.

It performs operations such as:

Connecting using API Key and Secret Key
Retrieving account balance
Fetching market data
Getting exchange information
Setting leverage
Setting isolated margin
Opening Futures orders
Cancelling pending orders
Checking open positions
Secure API Key Management

API credentials are never hardcoded.

Instead, they are loaded from a .env file using:

python-dotenv

This keeps API keys secure and prevents accidental exposure in source code.

Public IP Verification

Before connecting to Binance, the bot determines and prints the machine's public IP address using the ipify API.

This is useful because Binance API keys are commonly restricted to whitelisted IP addresses.

Market Data Collection

Every minute, the bot downloads the latest 40 one-minute candlesticks (OHLCV) for:

BTCUSDT Futures

The candlestick data includes:

Open
High
Low
Close
Volume

The data is converted into a Pandas DataFrame for further analysis.

Technical Indicator Calculation

The trading strategy is based on the Exponential Moving Average (EMA).

Instead of calculating EMA using closing price, the bot first computes:

HL2 = (High + Low) / 2

This average price is then used as the EMA input.

Two EMAs are calculated:

EMA 5
EMA 34

using the pandas-ta technical analysis library.

Trading Strategy

The strategy is an EMA crossover system.

Long Entry

A BUY order is generated when:

EMA(5) > EMA(34)

This indicates short-term bullish momentum.

Short Entry

A SELL order is generated when:

EMA(34) > EMA(5)

This indicates bearish momentum.

No Trade

If neither condition exists, the bot waits until the next candle.

Order Placement

Whenever a signal is detected, the bot:

Retrieves the current mark price
Retrieves Binance price precision
Retrieves Binance quantity precision
Rounds values according to exchange rules
Places a LIMIT Futures Order
Uses Good Till Cancelled (GTC) as the order type

Supported order directions:

BUY
SELL
Account Management

The bot periodically checks the Futures wallet balance.

It prints the available USDT balance to the console.

This helps monitor remaining trading capital while the bot is running.

Position Monitoring

Before starting the trading loop, the bot checks whether an existing Futures position is already open.

If a position exists, it can cancel any outstanding open orders before continuing.

This helps prevent duplicate pending orders.

Exchange Configuration

Before trading begins, the bot automatically configures:

Leverage

Leverage is set to:

5x
Margin Mode

Margin mode is configured as:

ISOLATED

This ensures each position uses isolated margin rather than cross margin.

Continuous Trading Loop

After initialization, the bot enters an infinite loop that runs every 60 seconds.

Each cycle performs the following sequence:

Download latest market data
Calculate EMA indicators
Display DataFrame
Retrieve account balance
Evaluate trading conditions (currently commented out in the source code)
Wait for one minute
Repeat
Main Functions
Function	Description
get_public_ip()	Retrieves public IP address
GET_ACCOUNT_BALANCE()	Displays available USDT balance
EMA_CALCULATOR()	Calculates EMA using HL2 price
DATA_FETCHER()	Downloads Binance candlestick data
SET_LEVERAGE()	Configures Futures leverage
SET_MARGIN_TYPE()	Sets isolated margin mode
GET_PRICE_PRECISION()	Retrieves exchange price precision
GET_QUANTITY_PRECISION()	Retrieves exchange quantity precision
OPEN_ORDER()	Places BUY or SELL limit orders
CHECK_POSITIONS()	Checks existing Futures positions
CLOSE_OPEN_ORDER()	Cancels pending open orders
TRADING_ALGO()	Implements the EMA crossover trading logic
Current Trading Parameters
Parameter	Value
Symbol	BTCUSDT
Market	Binance USDT-M Futures
Interval	1 Minute
Candles Used	40
Indicator	EMA (5, 34)
Price Source	HL2 ((High + Low)/2)
Order Type	LIMIT
Margin Mode	ISOLATED
Leverage	5x
Position Size	5 USDT (configured as volume)
Libraries Used
pandas
pandas-ta
python-binance (USDT Futures SDK)
python-dotenv
requests
os
time
Current Status

The bot is currently structured as a foundation for automated trading. It successfully handles data retrieval, indicator calculation, exchange configuration, account monitoring, and order management. However, the actual execution of the trading strategy is currently disabled because the call to TRADING_ALGO(df) in the main loop is commented out. As written, the bot fetches and displays market data and account information every minute but does not place trades unless that line is uncommented.

Overall, this project serves as a clean, modular starting point for a Binance Futures trading system that can be expanded with additional risk management features such as stop-loss, take-profit, trailing stop, position sizing, logging, backtesting, and more sophisticated trading strategies.
