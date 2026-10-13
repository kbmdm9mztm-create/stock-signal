import yfinance as yf


def get_prices(ticker, period="1mo"):
    """Download daily prices for one ticker."""
    data = yf.Ticker(ticker).history(period=period)
    return data
def get_earnings(ticker, limit=12):
    """Download past earnings: expected vs actual profit per share."""
    data = yf.Ticker(ticker).get_earnings_dates(limit=limit)
    if data is None or data.empty:
        return None
    # Drop future reports, which have no actual number yet
    data = data.dropna(subset=["Reported EPS", "EPS Estimate"])
    return data
def get_quote(ticker):
    """Latest price and % change versus yesterday's close."""
    info = yf.Ticker(ticker).fast_info
    last = float(info["last_price"])
    prev = float(info["previous_close"])
    change = (last - prev) / prev * 100
    return {"ticker": ticker, "price": round(last, 2), "change": round(change, 2)}
if __name__ == "__main__":
    ticker = input("Enter a ticker (e.g. AAPL): ").upper()
    prices = get_prices(ticker)

    if prices.empty:
        print("No data found. Check the ticker and try again.")
    else:
        print(prices[["Open", "Close", "Volume"]])