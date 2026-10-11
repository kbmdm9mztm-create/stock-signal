from flask import Flask, jsonify
from prices import get_prices

app = Flask(__name__)


@app.route("/prices/<ticker>")
def prices_route(ticker):
    ticker = ticker.upper()
    data = get_prices(ticker)

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