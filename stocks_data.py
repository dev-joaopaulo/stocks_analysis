import yfinance as yf


def get_data_from_ticker(ticker_symbol, interval, period):
    ticker = ticker_symbol + ".SA"
    stock = yf.Ticker(ticker)
    return stock.history(interval=interval, period=period)

