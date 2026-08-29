import os
import time
import json
import logging
from typing import Dict, Any, Optional
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder="static", static_url_path="")
CORS(app)

# In-memory TTL Cache
CACHE: Dict[str, Dict[str, Any]] = {}

def get_from_cache(key: str, max_age_seconds: int = 30) -> Optional[Any]:
    entry = CACHE.get(key)
    if entry and (time.time() - entry["timestamp"] < max_age_seconds):
        return entry["data"]
    return None

def set_cache(key: str, data: Any):
    CACHE[key] = {
        "timestamp": time.time(),
        "data": data
    }

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept": "application/json, text/plain, */*"
}

@app.route("/")
def serve_index():
    return send_from_directory("static", "index.html")

@app.route("/api/search")
def search_tickers():
    query = request.args.get("q", "").strip()
    if not query:
        return jsonify([])

    cache_key = f"search:{query.lower()}"
    cached = get_from_cache(cache_key, max_age_seconds=300)
    if cached:
        return jsonify(cached)

    try:
        url = f"https://query2.finance.yahoo.com/v1/finance/search?q={query}&quotesCount=10&newsCount=0"
        resp = requests.get(url, headers=HEADERS, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            quotes = data.get("quotes", [])
            results = []
            for item in quotes:
                symbol = item.get("symbol")
                shortname = item.get("shortname") or item.get("longname") or symbol
                quote_type = item.get("quoteType", "EQUITY")
                exchange = item.get("exchange", "")
                if symbol:
                    results.append({
                        "symbol": symbol,
                        "name": shortname,
                        "type": quote_type,
                        "exchange": exchange
                    })
            set_cache(cache_key, results)
            return jsonify(results)
    except Exception as e:
        logger.warning(f"Error in search API: {e}")

    # Fallback to local common list if network search failed
    popular = [
        {"symbol": "AAPL", "name": "Apple Inc.", "type": "EQUITY", "exchange": "NASDAQ"},
        {"symbol": "MSFT", "name": "Microsoft Corporation", "type": "EQUITY", "exchange": "NASDAQ"},
        {"symbol": "NVDA", "name": "NVIDIA Corporation", "type": "EQUITY", "exchange": "NASDAQ"},
        {"symbol": "AMZN", "name": "Amazon.com Inc.", "type": "EQUITY", "exchange": "NASDAQ"},
        {"symbol": "GOOGL", "name": "Alphabet Inc. (Class A)", "type": "EQUITY", "exchange": "NASDAQ"},
        {"symbol": "META", "name": "Meta Platforms Inc.", "type": "EQUITY", "exchange": "NASDAQ"},
        {"symbol": "TSLA", "name": "Tesla Inc.", "type": "EQUITY", "exchange": "NASDAQ"},
        {"symbol": "SPY", "name": "SPDR S&P 500 ETF Trust", "type": "ETF", "exchange": "NYSEArca"},
        {"symbol": "QQQ", "name": "Invesco QQQ Trust", "type": "ETF", "exchange": "NASDAQ"},
        {"symbol": "BTC-USD", "name": "Bitcoin USD", "type": "CRYPTOCURRENCY", "exchange": "CCC"}
    ]
    filtered = [s for s in popular if query.lower() in s["symbol"].lower() or query.lower() in s["name"].lower()]
    return jsonify(filtered)

@app.route("/api/quote")
def get_quote():
    symbol = request.args.get("symbol", "AAPL").strip().upper()
    cache_key = f"quote:{symbol}"
    cached = get_from_cache(cache_key, max_age_seconds=15)
    if cached:
        return jsonify(cached)

    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range=1d"
        resp = requests.get(url, headers=HEADERS, timeout=6)
        if resp.status_code == 200:
            data = resp.json()
            result = data.get("chart", {}).get("result", [])
            if result:
                meta = result[0].get("meta", {})
                current_price = meta.get("regularMarketPrice", 0.0)
                prev_close = meta.get("chartPreviousClose") or meta.get("previousClose") or current_price
                change = current_price - prev_close if current_price and prev_close else 0.0
                change_pct = (change / prev_close * 100) if prev_close else 0.0

                indicators = result[0].get("indicators", {})
                quote_data = indicators.get("quote", [{}])[0]
                day_high = max(quote_data.get("high", [meta.get("regularMarketDayHigh", current_price)]) or [current_price])
                day_low = min(quote_data.get("low", [meta.get("regularMarketDayLow", current_price)]) or [current_price])
                volume = meta.get("regularMarketVolume", 0)

                quote_obj = {
                    "symbol": symbol,
                    "companyName": meta.get("shortName") or meta.get("longName") or symbol,
                    "currency": meta.get("currency", "USD"),
                    "exchangeName": meta.get("exchangeName", ""),
                    "price": round(current_price, 2),
                    "change": round(change, 2),
                    "changePercent": round(change_pct, 2),
                    "previousClose": round(prev_close, 2) if prev_close else None,
                    "open": round(meta.get("regularMarketDayOpen", current_price), 2) if meta.get("regularMarketDayOpen") else None,
                    "dayHigh": round(day_high if day_high is not None else current_price, 2),
                    "dayLow": round(day_low if day_low is not None else current_price, 2),
                    "fiftyTwoWeekHigh": round(meta.get("fiftyTwoWeekHigh", current_price), 2) if meta.get("fiftyTwoWeekHigh") else None,
                    "fiftyTwoWeekLow": round(meta.get("fiftyTwoWeekLow", current_price), 2) if meta.get("fiftyTwoWeekLow") else None,
                    "volume": volume,
                    "marketCap": meta.get("marketCap", None),
                    "timezone": meta.get("exchangeTimezoneName", "UTC"),
                    "lastUpdated": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
                }
                set_cache(cache_key, quote_obj)
                return jsonify(quote_obj)
    except Exception as e:
        logger.warning(f"Error fetching quote for {symbol}: {e}")

    # Return structured error if not found
    return jsonify({
        "error": f"Failed to retrieve quote for {symbol}",
        "symbol": symbol,
        "price": 0.0,
        "change": 0.0,
        "changePercent": 0.0
    }), 404

@app.route("/api/history")
def get_history():
    symbol = request.args.get("symbol", "AAPL").strip().upper()
    range_val = request.args.get("range", "1mo").strip() # 1d, 5d, 1mo, 3mo, 6mo, 1y, 5y, max
    interval = request.args.get("interval", "").strip()

    # Map sensible intervals if not provided
    if not interval:
        if range_val in ["1d"]:
            interval = "5m"
        elif range_val in ["5d"]:
            interval = "15m"
        elif range_val in ["1mo", "3mo"]:
            interval = "1d"
        elif range_val in ["6mo", "1y"]:
            interval = "1d"
        elif range_val in ["5y", "max"]:
            interval = "1wk"
        else:
            interval = "1d"

    cache_key = f"history:{symbol}:{range_val}:{interval}"
    cached = get_from_cache(cache_key, max_age_seconds=60)
    if cached:
        return jsonify(cached)

    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?range={range_val}&interval={interval}&includePrePost=false"
        resp = requests.get(url, headers=HEADERS, timeout=8)
        if resp.status_code == 200:
            data = resp.json()
            result = data.get("chart", {}).get("result", [])
            if result:
                item = result[0]
                timestamps = item.get("timestamp", [])
                indicators = item.get("indicators", {})
                quote = indicators.get("quote", [{}])[0]
                opens = quote.get("open", [])
                highs = quote.get("high", [])
                lows = quote.get("low", [])
                closes = quote.get("close", [])
                volumes = quote.get("volume", [])

                candles = []
                for i in range(len(timestamps)):
                    o = opens[i] if i < len(opens) else None
                    h = highs[i] if i < len(highs) else None
                    l = lows[i] if i < len(lows) else None
                    c = closes[i] if i < len(closes) else None
                    v = volumes[i] if i < len(volumes) else 0

                    if c is not None and o is not None:
                        candles.append({
                            "time": timestamps[i],
                            "open": round(o, 2),
                            "high": round(h, 2) if h is not None else round(c, 2),
                            "low": round(l, 2) if l is not None else round(c, 2),
                            "close": round(c, 2),
                            "volume": int(v) if v else 0
                        })

                response_data = {
                    "symbol": symbol,
                    "range": range_val,
                    "interval": interval,
                    "currency": item.get("meta", {}).get("currency", "USD"),
                    "candles": candles
                }
                set_cache(cache_key, response_data)
                return jsonify(response_data)
    except Exception as e:
        logger.warning(f"Error fetching chart history for {symbol}: {e}")

    return jsonify({"error": f"Failed to retrieve chart history for {symbol}", "candles": []}), 500

@app.route("/api/market-summary")
def get_market_summary():
    cache_key = "market_summary"
    cached = get_from_cache(cache_key, max_age_seconds=30)
    if cached:
        return jsonify(cached)

    symbols = [
        {"symbol": "^GSPC", "label": "S&P 500"},
        {"symbol": "^DJI", "label": "Dow Jones"},
        {"symbol": "^IXIC", "label": "Nasdaq"},
        {"symbol": "^RUT", "label": "Russell 2000"},
        {"symbol": "BTC-USD", "label": "Bitcoin"},
        {"symbol": "ETH-USD", "label": "Ethereum"},
        {"symbol": "GC=F", "label": "Gold"},
        {"symbol": "CL=F", "label": "Crude Oil"}
    ]

    movers_tickers = ["NVDA", "AAPL", "TSLA", "AMD", "MSFT", "AMZN", "META", "GOOGL", "NFLX", "PLTR", "INTC", "COIN"]

    summary = {
        "indices": [],
        "popular": []
    }

    # Fetch indices
    for item in symbols:
        sym = item["symbol"]
        try:
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?interval=1d&range=1d"
            resp = requests.get(url, headers=HEADERS, timeout=4)
            if resp.status_code == 200:
                result = resp.json().get("chart", {}).get("result", [])
                if result:
                    meta = result[0].get("meta", {})
                    price = meta.get("regularMarketPrice", 0.0)
                    prev = meta.get("chartPreviousClose") or meta.get("previousClose") or price
                    chg = price - prev if price and prev else 0.0
                    chg_pct = (chg / prev * 100) if prev else 0.0
                    summary["indices"].append({
                        "symbol": sym,
                        "name": item["label"],
                        "price": round(price, 2),
                        "change": round(chg, 2),
                        "changePercent": round(chg_pct, 2)
                    })
        except Exception:
            pass

    # Fetch popular movers
    for sym in movers_tickers:
        try:
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?interval=1d&range=1d"
            resp = requests.get(url, headers=HEADERS, timeout=3)
            if resp.status_code == 200:
                result = resp.json().get("chart", {}).get("result", [])
                if result:
                    meta = result[0].get("meta", {})
                    price = meta.get("regularMarketPrice", 0.0)
                    prev = meta.get("chartPreviousClose") or meta.get("previousClose") or price
                    chg = price - prev if price and prev else 0.0
                    chg_pct = (chg / prev * 100) if prev else 0.0
                    summary["popular"].append({
                        "symbol": sym,
                        "name": meta.get("shortName") or sym,
                        "price": round(price, 2),
                        "change": round(chg, 2),
                        "changePercent": round(chg_pct, 2),
                        "volume": meta.get("regularMarketVolume", 0)
                    })
        except Exception:
            pass

    set_cache(cache_key, summary)
    return jsonify(summary)

@app.route("/api/news")
def get_news():
    symbol = request.args.get("symbol", "").strip().upper()
    cache_key = f"news:{symbol or 'market'}"
    cached = get_from_cache(cache_key, max_age_seconds=180)
    if cached:
        return jsonify(cached)

    news_items = []
    try:
        query = symbol if symbol else "market stocks investing"
        url = f"https://query2.finance.yahoo.com/v1/finance/search?q={query}&newsCount=8"
        resp = requests.get(url, headers=HEADERS, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            raw_news = data.get("news", [])
            for n in raw_news:
                news_items.append({
                    "title": n.get("title"),
                    "publisher": n.get("publisher"),
                    "link": n.get("link"),
                    "providerPublishTime": n.get("providerPublishTime"),
                    "thumbnail": n.get("thumbnail", {}).get("resolutions", [{}])[0].get("url") if n.get("thumbnail") else None
                })
    except Exception as e:
        logger.warning(f"Error fetching news: {e}")

    # Fallback placeholder news if API returns empty
    if not news_items:
        news_items = [
            {
                "title": f"Market Analysis: Key tech stocks and macro factors to watch this week",
                "publisher": "Market Pulse",
                "link": "https://finance.yahoo.com",
                "providerPublishTime": int(time.time()) - 3600
            },
            {
                "title": f"Global markets digest latest economic updates and central bank outlook",
                "publisher": "Financial Times Wire",
                "link": "https://finance.yahoo.com",
                "providerPublishTime": int(time.time()) - 7200
            }
        ]

    set_cache(cache_key, news_items)
    return jsonify(news_items)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"\n=======================================================")
    print(f"🚀 Free Stock Viewer is running at: http://127.0.0.1:{port}")
    print(f"=======================================================\n")
    app.run(host="0.0.0.0", port=port, debug=False)
