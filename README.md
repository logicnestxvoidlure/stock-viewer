# 📈 StockPulse — Free Stock Viewer & Real-Time Market Terminal

**StockPulse** is a free, lightweight stock market dashboard built for anyone who wants to keep an eye on the markets without dealing with complicated tools or paid API keys.

You can search for stocks, check real-time prices, view historical performance, explore interactive charts, look at key financial metrics, track market movers, build a personal watchlist, and stay up to date with financial news — all from one place.

## 🌐 Live Demo

Want to try it out?

**StockPulse is available online and ready to use:**

👉 **https://stock-viewer-x6g3.onrender.com/**

No installation is required for the live version. Open the site, search for a ticker such as `AAPL`, and start exploring the market data.

---

## ✨ Features

* **Real-Time & Historical Market Data** — View current prices, daily highs and lows, opening prices, previous closes, trading volume, 52-week ranges, market caps, and more.
* **Multiple Timeframes** — Switch between `1D`, `5D`, `1M`, `3M`, `6M`, `1Y`, `5Y`, and `MAX`.
* **Interactive Charts** — Switch between Area/Line and Candlestick charts, with optional SMA 20 and volume data.
* **Detailed Chart Hovering** — Inspect exact OHLCV information while moving across the chart.
* **Market Overview** — Follow major indexes and assets including the S&P 500, Dow Jones, Nasdaq, Russell 2000, Bitcoin, Gold, and Crude Oil.
* **Quick Search** — Find stocks, ETFs, crypto pairs, and indexes using autocomplete.
* **Market Movers** — Check the current top gainers, losers, and popular stocks.
* **Watchlist** — Star stocks you want to keep an eye on. Your watchlist is saved in your browser automatically.
* **Financial News** — View recent market and stock-specific headlines.
* **CSV Export** — Export historical market data with one click.
* **Responsive Dark UI** — A clean trading-style interface designed for both desktop and mobile.

---

## 🚀 Getting Started

If you want to run StockPulse yourself, you can either use the included Windows batch file or start it from the command line.

### Windows

Run `run.bat` from the project folder. It will activate the virtual environment and start the server.

### Command Line

```bash
cd /d "%USERPROFILE%\Downloads\StockPulse"

.\venv\Scripts\activate

python app.py
```

Then open:

`http://localhost:5000`

---

## 🔌 API

StockPulse also provides a REST API for accessing market data.

### Quote

```http
GET /api/quote?symbol=AAPL
```

Returns the latest price and key information for a stock.

### Historical Data

```http
GET /api/history?symbol=AAPL&range=1mo&interval=1d
```

Returns historical OHLCV data.

### Search

```http
GET /api/search?q=apple
```

Searches for supported stocks, ETFs, crypto pairs, and other symbols.

### Market Summary

```http
GET /api/market-summary
```

Returns major market indexes and current market movers.

### News

```http
GET /api/news?symbol=AAPL
```

Returns recent financial news for the requested ticker.

---

## 🛠️ Built With

### Backend

* Python
* Flask
* Flask-CORS
* Requests

### Frontend

* HTML5
* Tailwind CSS
* Lucide Icons
* Custom HTML5 Canvas chart engine

StockPulse keeps things simple: **search a ticker, check the data, explore the chart, and stay on top of the market.**
