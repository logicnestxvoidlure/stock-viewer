# 📈 StockPulse — Free Stock Viewer & Real-Time Market Terminal

**StockPulse** is a free, lightweight stock market dashboard built for anyone who wants to keep an eye on the markets without dealing with complicated tools or paid API keys.

You can search for stocks, check real-time prices, view historical performance, explore interactive charts, look at key financial metrics, track market movers, build a personal watchlist, and stay up to date with the latest financial news — all from one place.

## ✨ Features

* **Real-Time & Historical Market Data** — View current prices, daily highs and lows, opening prices, previous closes, trading volume, 52-week ranges, market caps, and more.
* **Multiple Timeframes** — Switch between `1D`, `5D`, `1M`, `3M`, `6M`, `1Y`, `5Y`, and `MAX` to see how a stock has performed over different periods.
* **Interactive Charts** — Use Area/Line or Candlestick charts to explore price movements. You can also enable an SMA 20 indicator and view trading volume directly on the chart.
* **Detailed Chart Hovering** — Move your cursor across the chart to see exact OHLCV information for individual points.
* **Market Overview** — Keep track of major benchmarks and assets such as the S&P 500, Dow Jones, Nasdaq, Russell 2000, Bitcoin, Gold, and Crude Oil.
* **Quick Search** — Find US and international stocks, ETFs, crypto pairs, and indices with the built-in search and autocomplete.
* **Market Movers** — Quickly see which stocks are gaining, losing, or getting the most attention through the Gainers, Losers, and Popular tabs.
* **Watchlist** — Star your favorite stocks and keep them saved automatically in your browser.
* **Financial News** — Read recent market and stock-specific news without leaving the dashboard.
* **CSV Export** — Export historical stock data as a CSV file with a single click.
* **Responsive Dark UI** — StockPulse uses a dark, trading-focused interface designed to work smoothly on both desktop and mobile.

---

## 🚀 Getting Started

There are a couple of simple ways to run StockPulse locally.

### Windows

If you're on Windows, you can simply run `run.bat`. It will activate the virtual environment and start the application automatically.

### Command Line

You can also start it manually:

```bash
cd /d "%USERPROFILE%\Downloads\StockPulse"

.\venv\Scripts\activate

python app.py
```

Once the server starts, open:

`http://localhost:5000`

---

## 🔌 API

StockPulse also provides a small REST API that the frontend uses to retrieve market information.

### Quote

```http
GET /api/quote?symbol=AAPL
```

Returns the latest price and key information for a stock.

### Historical Data

```http
GET /api/history?symbol=AAPL&range=1mo&interval=1d
```

Returns historical OHLCV data that can be used to build price charts.

### Search

```http
GET /api/search?q=apple
```

Searches for stocks, ETFs, crypto pairs, and other supported symbols.

### Market Summary

```http
GET /api/market-summary
```

Returns major market indexes and current market movers.

### News

```http
GET /api/news?symbol=AAPL
```

Returns recent financial news related to the requested ticker.

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

StockPulse is designed to stay simple: **search a ticker, see the data, understand the market, and move on.**
