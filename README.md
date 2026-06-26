# 🚀 BTCUSDT Binance Futures Trading Python Algobot

A Python-based **Binance USDT-M Futures Trading Bot** that automates cryptocurrency trading using an **Exponential Moving Average (EMA) crossover strategy**.

The bot connects to the Binance Futures API, retrieves live BTCUSDT market data every minute, calculates technical indicators, monitors account information, and places buy or sell orders automatically when trading conditions are met.

The application is designed with modular functions, making it easy to understand, customize, and extend with additional trading strategies or risk management features.

---

# 📌 Features

- Binance USDT-M Futures API integration
- Automatic market data collection
- EMA crossover strategy
- Live account balance monitoring
- Automatic leverage configuration
- Automatic margin type configuration
- Position monitoring
- Order placement
- Order cancellation
- Exchange precision handling
- Secure API key management using `.env`
- Continuous trading loop

---

# 🛠️ Technologies Used

- Python 3.x
- Pandas
- Pandas TA
- Binance Futures Python SDK
- Python Dotenv
- Requests

---

# 📂 Project Structure

```
.
├── main_block.py        # Main trading bot
├── .env                 # Binance API credentials
├── requirements.txt
└── README.md
```

---

# ⚙️ How It Works

The trading bot performs the following sequence continuously:

1. Connects to Binance Futures.
2. Retrieves the public IP address.
3. Configures leverage.
4. Configures isolated margin.
5. Downloads the latest market data.
6. Calculates EMA indicators.
7. Checks account balance.
8. Evaluates trading conditions.
9. Places orders when conditions are satisfied.
10. Waits for the next candle.
11. Repeats the process.

---

# 🔐 Secure API Management

API credentials are stored securely inside a `.env` file instead of being hardcoded.

Example:

```env
API_KEY=YOUR_BINANCE_API_KEY
API_SECRET=YOUR_BINANCE_SECRET_KEY
```

---

# 🌐 Public IP Verification

The bot retrieves and displays the machine's public IP address before connecting to Binance.

This helps verify that the IP matches the Binance API whitelist.

---

# 📈 Market Data Collection

The bot downloads the latest **40 one-minute candlesticks** for **BTCUSDT Futures**.

Each candle contains:

- Open
- High
- Low
- Close
- Volume

The downloaded data is converted into a Pandas DataFrame for technical analysis.

---

# 📊 Technical Indicators

The strategy uses **Exponential Moving Averages (EMA)** calculated from the **HL2 price**, where:

```
HL2 = (High + Low) / 2
```

The following EMAs are calculated:

- EMA(5)
- EMA(34)

The calculations are performed using the **Pandas TA** library.

---

# 📉 Trading Strategy

The bot implements a simple EMA crossover strategy.

## Buy Signal

A **BUY** order is generated when:

```
EMA(5) > EMA(34)
```

This indicates bullish momentum.

---

## Sell Signal

A **SELL** order is generated when:

```
EMA(5) < EMA(34)
```

This indicates bearish momentum.

---

## No Trade

If neither condition is met, the bot waits for the next candle.

---

# 💰 Account Monitoring

The bot periodically checks the Futures account balance and displays the available USDT balance.

This allows the user to monitor available trading capital while the bot is running.

---

# ⚙️ Exchange Configuration

Before trading begins, the bot automatically configures the trading account.

### Margin Type

```
ISOLATED
```

### Leverage

```
5x
```

---

# 📦 Order Placement

When a valid signal is detected, the bot performs the following:

- Retrieves the latest market price
- Retrieves Binance price precision
- Retrieves Binance quantity precision
- Rounds values according to Binance exchange rules
- Places a LIMIT order
- Uses Good Till Cancelled (GTC)

Supported order types:

- BUY
- SELL

---

# 📌 Position Management

The bot checks for existing positions before opening a new trade.

It can also cancel existing open orders to avoid duplicate entries.

---

# 🔄 Continuous Trading Loop

The bot runs continuously in an infinite loop.

Each cycle performs:

```
Download Market Data
        ↓
Calculate EMA
        ↓
Display Data
        ↓
Check Balance
        ↓
Evaluate Strategy
        ↓
Place Order (if signal exists)
        ↓
Wait 60 Seconds
        ↓
Repeat
```

---

# 📋 Main Functions

| Function | Description |
|----------|-------------|
| `get_public_ip()` | Retrieves the machine's public IP address |
| `GET_ACCOUNT_BALANCE()` | Displays available Futures wallet balance |
| `DATA_FETCHER()` | Downloads Binance candlestick data |
| `EMA_CALCULATOR()` | Calculates EMA indicators |
| `SET_LEVERAGE()` | Sets Futures leverage |
| `SET_MARGIN_TYPE()` | Configures isolated margin mode |
| `GET_PRICE_PRECISION()` | Retrieves price precision |
| `GET_QUANTITY_PRECISION()` | Retrieves quantity precision |
| `OPEN_ORDER()` | Places BUY or SELL orders |
| `CHECK_POSITIONS()` | Checks existing Futures positions |
| `CLOSE_OPEN_ORDER()` | Cancels pending orders |
| `TRADING_ALGO()` | Implements the EMA crossover strategy |

---

# 📊 Trading Parameters

| Parameter | Value |
|-----------|-------|
| Exchange | Binance Futures |
| Symbol | BTCUSDT |
| Market | USDT-M Futures |
| Candle Interval | 1 Minute |
| Candles Downloaded | 40 |
| Indicator | EMA (5,34) |
| Price Source | HL2 |
| Margin Type | ISOLATED |
| Leverage | 5x |
| Order Type | LIMIT |
| Time In Force | GTC |

---

# ▶️ Running the Bot

Install the required packages:

```bash
pip install -r requirements.txt
```

Run the bot:

```bash
python main_block.py
```

---

# 📈 Future Improvements

Some enhancements that can be added include:

- Stop Loss
- Take Profit
- Trailing Stop Loss
- Dynamic Position Sizing
- ATR-based Risk Management
- Telegram Notifications
- Email Alerts
- Logging
- Trade History
- Backtesting
- Multiple Trading Strategies
- WebSocket Price Streaming
- Multi-Symbol Trading
- Dashboard for Monitoring

---

# ⚠️ Disclaimer

This project is intended for educational and research purposes only.

Cryptocurrency trading involves significant financial risk. Use this software at your own risk. The author is not responsible for any financial losses resulting from the use of this trading bot.

---

# 📄 License

This project is licensed under the MIT License.

---

## ⭐ If you find this project useful, consider giving it a star on GitHub!
