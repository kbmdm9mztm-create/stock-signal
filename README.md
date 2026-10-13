# Stock Signal

A learning project: a small website that shows stock prices, compares
analysts' expected earnings with what companies actually reported, and
checks what the price did afterwards.

**This is not trading advice.** It was built to learn, and it is not a
tool for making money.

## What it does

- Price chart for any ticker (last month)
- Earnings table: expected vs actual profit per share, and the surprise %
- History test: how often the price rose 1 and 5 days after a big surprise
- Live page: auto-refreshing bar chart of today's % change (green up, red down)

## Built with

- Python, Flask (the server)
- yfinance (price and earnings data from Yahoo Finance)
- HTML, CSS, JavaScript and Chart.js (the pages)

## How to run it

1. Install Python 3
2. Install the libraries: `py -m pip install flask yfinance lxml`
3. Start the server: `py app.py`
4. Open http://127.0.0.1:8000/ in your browser

## Limits (be honest)

- Free Yahoo data can be delayed, patchy, or break without warning.
- One company has too few earnings reports to prove anything.
- Fees, spreads, and taxes would eat small gains in real trading.

## What I learned

I learned about html , java and css in this project and have basic idea on debugging code and how to make a good enough project by myself with the help of claude haha

## What I would do next

i am stopping this project here for now i will return and i will most probably add more company and make it user friendly and work on front end