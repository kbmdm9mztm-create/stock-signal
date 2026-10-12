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

if __name__ == "__main__":
    ticker = input("Enter a ticker (e.g. AAPL): ").upper()
    prices = get_prices(ticker)

    if prices.empty:
        print("No data found. Check the ticker and try again.")
    else:
        print(prices[["Open", "Close", "Volume"]])