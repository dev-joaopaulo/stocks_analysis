import yfinance as yf


def get_data_from_ticker(ticker_symbol, interval, period):
    ticker = ticker_symbol + ".SA"
    stock = yf.Ticker(ticker)
    return stock.history(interval=interval, period=period)


def find_stocks_with_high_volume(ticker_symbols, interval, period, moving_average_days):
    high_volume_stocks = []
    for ticker in ticker_symbols:
        data = get_data_from_ticker(ticker, interval, period)

        # Calcula a média móvel e o desvio padrão do volume
        data['Volume MA'] = data['Volume'].rolling(window=moving_average_days).mean()
        volume_std_dev = data['Volume'].rolling(window=moving_average_days).std()

        # Verifica se o volume mais recente é maior que a média móvel mais um desvio padrão
        if data['Volume'].iloc[-1] > data['Volume MA'].iloc[-1] + volume_std_dev.iloc[-1]:
            high_volume_stocks.append(ticker)

    return high_volume_stocks
