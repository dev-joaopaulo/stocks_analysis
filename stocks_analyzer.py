from stocks_data import get_data_from_ticker
from rsi_indicator import *


def analyze_rsi_opportunities_from_tickers(tickers, interval, period, upper_rsi_limit=0.9, lower_rsi_limit=0.10):
    overbought_tickers = []
    oversold_tickers = []
    for ticker in tickers:
        try:
            historical_data = get_data_from_ticker(ticker, interval, period)
        except:
            print(f"Not possible to get data from {ticker}")
            break
        rsi = calculate_rsi(historical_data)
        upper_threshold = get_upper_threshold_rsi(rsi, upper_rsi_limit)
        lower_threshold = get_lower_threshold_rsi(rsi, lower_rsi_limit)
        last_result = rsi.iloc[-1]
        if last_result < lower_threshold:
            oversold_tickers.append(ticker)
        if last_result > upper_threshold:
            overbought_tickers.append(ticker)
    return [overbought_tickers, oversold_tickers]


def print_rsi_opportunity_analysis(rsi_opportunity_analysis):
    print("overbought tickers: " + str(rsi_opportunity_analysis[0]))
    print("oversold tickers: " + str(rsi_opportunity_analysis[1]))
