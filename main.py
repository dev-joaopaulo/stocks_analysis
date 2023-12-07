from tickers import *
from stocks_analyzer import *

import warnings

# Ignora FutureWarnings específicos relacionados a yfinance
warnings.filterwarnings("ignore", category=FutureWarning, module="yfinance.*")


if __name__ == '__main__':
    interval = "1wk"
    ifix_analysis = analyze_rsi_opportunities_from_tickers(IFIX, interval, "2y")
    idiv_analysis = analyze_rsi_opportunities_from_tickers(IDIV, interval, "5y", lower_rsi_limit=0.15)
    smll_analysis = analyze_rsi_opportunities_from_tickers(SMLL, interval, "2y")
    print("____________IFIX_______________")
    print_rsi_opportunity_analysis(ifix_analysis)
    print("____________IDIV_______________")
    print_rsi_opportunity_analysis(idiv_analysis)
    print("____________SMLL_______________")
    print_rsi_opportunity_analysis(smll_analysis)


