import time
from flask import Flask, jsonify, request
from prices import get_prices , get_earnings, get_quote

app = Flask(__name__)

cache = {}  # remembers answers: {ticker: (time_saved, data)}
CACHE_SECONDS = 300  # remember for 5 minutes


@app.route("/")
def home():
    return app.send_static_file("index.html")


@app.route("/prices/<ticker>")
def prices_route(ticker):
    ticker = ticker.upper()

    if ticker in cache and time.time() - cache[ticker][0] < CACHE_SECONDS:
        data = cache[ticker][1]
    else:
        data = get_prices(ticker)
        cache[ticker] = (time.time(), data)

    if data.empty:
        return jsonify({"error": "No data found"}), 404

    rows = []
    for date, row in data.iterrows():
        rows.append({
            "date": date.strftime("%Y-%m-%d"),
            "close": round(float(row["Close"]), 2),
        })

    return jsonify({"ticker": ticker, "prices": rows})
@app.route("/earnings/<ticker>")
def earnings_route(ticker):
    ticker = ticker.upper()

    try:
        data = get_earnings(ticker)
    except Exception:
        return jsonify({"error": "Could not get earnings data"}), 500

    if data is None or data.empty:
        return jsonify({"error": "No earnings data found"}), 404

    rows = []
    for date, row in data.iterrows():
        expected = float(row["EPS Estimate"])
        actual = float(row["Reported EPS"])

        if expected != 0:
            surprise = round((actual - expected) / abs(expected) * 100, 1)
        else:
            surprise = None

        rows.append({
            "date": date.strftime("%Y-%m-%d"),
            "expected": round(expected, 2),
            "actual": round(actual, 2),
            "surprise": surprise,
        })

    return jsonify({"ticker": ticker, "earnings": rows})
def summarize(items):
    if not items:
        return None
    n = len(items)
    return {
        "count": n,
        "up_day1": sum(1 for r in items if r["day1"] > 0),
        "up_day5": sum(1 for r in items if r["day5"] > 0),
        "avg_day1": round(sum(r["day1"] for r in items) / n, 2),
        "avg_day5": round(sum(r["day5"] for r in items) / n, 2),
    }


@app.route("/history/<ticker>")
def history_route(ticker):
    ticker = ticker.upper()

    try:
        earnings = get_earnings(ticker, limit=20)
        prices = get_prices(ticker, period="5y")
    except Exception:
        return jsonify({"error": "Could not get data"}), 500

    if earnings is None or earnings.empty or prices.empty:
        return jsonify({"error": "Not enough data for a history test"}), 404

    # Make price dates plain dates (no time zone, no clock time)
    closes = prices["Close"].copy()
    closes.index = closes.index.tz_localize(None).normalize()

    rows = []
    for date, row in earnings.iterrows():
        expected = float(row["EPS Estimate"])
        actual = float(row["Reported EPS"])
        if expected == 0:
            continue

        surprise = (actual - expected) / abs(expected) * 100
        report_day = date.tz_localize(None).normalize()

        # Find the first trading day on or after the report date
        pos = closes.index.searchsorted(report_day)
        if pos < 1 or pos + 5 >= len(closes):
            continue  # not enough price data around this report

        base = closes.iloc[pos - 1]  # close the day before the report
        rows.append({
            "surprise": surprise,
            "day1": (closes.iloc[pos + 1] / base - 1) * 100,
            "day5": (closes.iloc[pos + 5] / base - 1) * 100,
        })

    positive = [r for r in rows if r["surprise"] > 5]
    negative = [r for r in rows if r["surprise"] < -5]

    return jsonify({
        "ticker": ticker,
        "reports_used": len(rows),
        "positive": summarize(positive),
        "negative": summarize(negative),
    })
quote_cache = {}
QUOTE_SECONDS = 15  # reuse an answer for 15 seconds


@app.route("/live")
def live_page():
    return app.send_static_file("live.html")


@app.route("/quotes")
def quotes_route():
    raw = request.args.get("tickers", "")
    tickers = [t.strip().upper() for t in raw.split(",") if t.strip()][:10]

    results = []
    for t in tickers:
        cached = quote_cache.get(t)
        if cached and time.time() - cached[0] < QUOTE_SECONDS:
            q = cached[1]
        else:
            try:
                q = get_quote(t)
            except Exception:
                q = None
            quote_cache[t] = (time.time(), q)
        if q:
            results.append(q)

    return jsonify({"quotes": results})
if __name__ == "__main__":
    app.run(debug=True, port=8000)