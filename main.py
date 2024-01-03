from rsi_backtest import make_extensive_test_ticker, backtest_rsi, make_extensive_test_tickers_list
import pandas as pd
import warnings

from stocks_data import find_stocks_with_high_volume
from tickers import *
from rsi_opportunity_analyzer import *

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

# Ignora FutureWarnings específicos relacionados a yfinance
warnings.filterwarnings("ignore", category=FutureWarning)

if __name__ == '__main__':
    interval = "1wk"

    # ifix_analysis = analyze_rsi_opportunities_from_tickers(IFIX, interval, "2y")
    # idiv_analysis = analyze_rsi_opportunities_from_tickers(IDIV, interval, "5y", lower_rsi_limit=0.15)
    # print("____________IFIX_______________")
    # print_rsi_opportunity_analysis(ifix_analysis)
    # print(f"IFIX com alto volume {find_stocks_with_high_volume(IFIX, '1d', '1mo', 10)}")
    # print("____________IDIV_______________")
    # print_rsi_opportunity_analysis(idiv_analysis)
    # print(f"IDIV com alto volume {find_stocks_with_high_volume(IDIV, '1d', '1mo', 10)}")

if __name__ == '__main__':
    ticker = "CMIG3"
    period = "15y"
    interval = "1wk"
    use_stop = True
    use_upper_threshold = True
    use_target = True
    min_holding_period = 4

    # print(f"____________backtest {ticker}_______________")
    # backtest = backtest_rsi(ticker, 1.2, period, interval, min_holding_period=min_holding_period, use_stop=use_stop,
    #                         use_upper_threshold=use_upper_threshold, use_target=use_target)
    # print(backtest)
    #
    # print(f"____________ticker_analysis_results {ticker}_______________")
    # ticker_analysis_results = make_extensive_test_ticker(ticker, period, interval,
    #                                                      min_holding_period=min_holding_period,
    #                                                      use_stop=use_stop, use_upper_threshold=use_upper_threshold,
    #                                                      use_target=use_target)
    # print(ticker_analysis_results)

    # if __name__ == '__main__':
    #     period = "15y"
    #     interval = "1wk"
    #     use_stop = True
    #     use_upper_threshold = True
    #     use_target = True
    #     min_holding_period = 4
    #
    # print(make_extensive_test_tickers_list(IDIV, period, interval, min_holding_period=min_holding_period,
    #                                        use_stop=use_stop, use_upper_threshold=use_upper_threshold,
    #                                        use_target=use_target))
