import yfinance as yf


def get_prices(ticker, period="1mo"):
    """Download daily prices for one ticker."""
    data = yf.Ticker(ticker).history(period=period)
    return data


if __name__ == "__main__":
    ticker = input("Enter a ticker (e.g. AAPL): ").upper()
    prices = get_prices(ticker)

    if prices.empty:
        print("No data found. Check the ticker and try again.")
    else:
        print(prices[["Open", "Close", "Volume"]])