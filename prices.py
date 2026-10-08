import yfinance as yf

# Pick a company by its ticker symbol (AAPL = Apple)
ticker = "AAPL"

# Download the last 1 month of daily prices
data = yf.Ticker(ticker).history(period="1mo")

print(data[["Open", "Close", "Volume"]])