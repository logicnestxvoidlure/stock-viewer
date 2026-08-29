📈 StockPulse — Free Stock Viewer & Real-Time Market Terminal
StockPulse is a free, fast, and easy-to-use stock market dashboard that brings live market data right to your browser—no credit card, no hidden fees, no paid API keys required.

Whether you're casually checking how your favorite stocks are doing or digging deeper into price trends, StockPulse has you covered. You can search for any stock, ETF, or crypto pair, view interactive charts, track market movers, save a personal watchlist, and catch up on the latest financial news—all from one clean, dark-themed interface.

✨ What You Can Do
Get real-time and historical stock data — including current price, daily high/low, open, previous close, trading volume, 52-week range, and market cap.

Choose your time horizon — quickly switch between 1D, 5D, 1M, 3M, 6M, 1Y, 5Y, or MAX views.

Explore interactive charts built with HTML5 Canvas:

Toggle between Area/Line and Candlestick views.

Add a 20-day Simple Moving Average (SMA) overlay to spot trends.

See volume as colored histogram bars that match each candle's direction.

Hover anywhere on the chart to see exact OHLCV (Open, High, Low, Close, Volume) values.

Watch major market indices in the ticker ribbon at the top — S&P 500, Dow Jones, Nasdaq, Russell 2000, Bitcoin, Gold, and Crude Oil.

Search instantly with autocomplete — works for US and global stocks, ETFs, crypto pairs, and indices.

Track what's moving the market — with one-click tabs for Top Gainers, Top Losers, and Most Popular stocks.

Build your watchlist — star your favorite stocks with a single click, and they'll stay saved in your browser (thanks to localStorage).

Read the latest financial news — headlines load automatically and link directly to full articles.

Download data — export historical OHLCV data to CSV with one click.

Enjoy a sleek, trader-friendly interface — dark/OLED aesthetics with neon accents, clean fonts (Plus Jakarta Sans & JetBrains Mono), and a responsive layout that works great on both desktop and mobile.

🚀 How to Get Started
Option 1: One-Click (Windows)
Just double-click run.bat in the project folder. It'll handle the virtual environment and launch the server for you.

Option 2: Manual (Command Line)
bash
# 1. Go to the project folder
cd /d "%USERPROFILE%\Downloads\StockPulse"

# 2. Activate the virtual environment
.\venv\Scripts\activate

# 3. Start the app
python app.py
Then open your browser and visit:
👉 http://localhost:5000

🔌 API Endpoints (for the curious)
GET /api/quote?symbol=AAPL — Get a real-time quote and key metrics for a ticker.

GET /api/history?symbol=AAPL&range=1mo&interval=1d — Get historical OHLCV candle data.

GET /api/search?q=apple — Autocomplete ticker suggestions as you type.

GET /api/market-summary — Get major index values and top movers.

GET /api/news?symbol=AAPL — Get recent news articles for a ticker.

🛠️ Built With
Backend: Python, Flask, Flask-CORS, Requests

Frontend: HTML5, Tailwind CSS, Lucide Icons, and a custom high-performance Canvas chart engine built from scratch

StockPulse is made for people who want to stay informed without the hassle. No subscriptions. No noise. Just clean, real-time market data at your fingertips.
