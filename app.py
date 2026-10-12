import time
from flask import Flask, jsonify
from prices import get_prices

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


if __name__ == "__main__":
    app.run(debug=True, port=8000)