# 📈 StockPulse — Free Stock Viewer & Real-Time Market Terminal

**StockPulse** is a lightweight, responsive, and completely free-to-use web-based stock market viewer and analytics dashboard. It allows anyone to search equities, view live/historical stock prices, interact with candlestick and area charts, inspect fundamental metrics, track market movers, manage a watchlist, and read financial news without requiring paid API keys.

---

## ✨ Features

- **100% Free Live & Historical Market Data**: Real-time quotes, day high/low, open, previous close, volume, 52-week ranges, and market capitalization.
- **Dynamic Timeframes**: `1D`, `5D`, `1M`, `3M`, `6M`, `1Y`, `5Y`, and `MAX`.
- **Interactive Canvas Chart Engine**:
  - Toggle between **Area / Line** and **Candlestick** chart modes.
  - Optional **SMA 20** (Simple Moving Average) trend overlay.
  - Dynamic Volume histogram bars colored according to candle direction.
  - Interactive crosshairs and hovering HUD with exact OHLCV details.
- **Top Market Ticker Ribbon**: Live index benchmarks (S&P 500, Dow Jones, Nasdaq, Russell 2000, Bitcoin, Gold, Crude Oil).
- **Search Autocomplete**: Fast lookup across US & global stocks, ETFs, crypto pairs, and indices.
- **Active Market Movers**: Instant tabbed switching between **Top Gainers**, **Top Losers**, and **Popular** equities.
- **Persistent Watchlist**: 1-click star / unstar stocks with automatic browser `localStorage` persistence.
- **Live Financial News**: Automatically loads recent market and ticker-specific headlines with direct links.
- **Data Export**: Export historical candle data to CSV with 1 click.
- **Dark / OLED Trading Aesthetics**: Modern neon accents, clean typography (Plus Jakarta Sans & JetBrains Mono), and responsive mobile/desktop layout.

---

## 🚀 How to Run

### Option 1: 1-Click Batch File (Windows)
Double-click `run.bat` in the project directory. It will activate the virtual environment and start the server.

### Option 2: Command Line

```bash
# 1. Navigate to the project directory
cd /d "%USERPROFILE%\Downloads\StockPulse"

# 2. Activate virtual environment
.\venv\Scripts\activate

# 3. Start the application
python app.py
```

Open your browser at:
👉 **`http://localhost:5000`**

---

## 🔌 API Endpoints

- `GET /api/quote?symbol=AAPL` — Real-time price quote and key fundamental metrics.
- `GET /api/history?symbol=AAPL&range=1mo&interval=1d` — Historical OHLCV candle data.
- `GET /api/search?q=apple` — Autocomplete ticker suggestions.
- `GET /api/market-summary` — Major indices and active market movers.
- `GET /api/news?symbol=AAPL` — Recent financial news articles.

---

## 🛠️ Tech Stack

- **Backend**: Python, Flask, Flask-CORS, Requests
- **Frontend**: HTML5, Tailwind CSS, Lucide Icons, Custom High-Performance HTML5 Canvas Chart Engine
