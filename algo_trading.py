import yfinance as yf
from pyalgotrade import strategy
from pyalgotrade.technical import ma
from pyalgotrade.barfeed import yahoofeed
from pyalgotrade.broker import backtesting
import matplotlib.pyplot as plt

from stocks_data import get_data_from_ticker, get_data_with_adj_close


class MyStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, smaPeriod):
        super(MyStrategy, self).__init__(feed)
        self.__instrument = instrument
        self.__sma = ma.SMA(feed[instrument].getCloseDataSeries(), smaPeriod)
        self.setUseAdjustedValues(True)
        self._portfolioValues = []

    def onBars(self, bars):
        bar = bars[self.__instrument]
        if self.__sma[-1] is None:
            return

        # Verifica se há posições longas ativas
        positions = self.getBroker().getPositions()
        if self.__instrument in positions:
            if bar.getPrice() < self.__sma[-1]:
                self.marketOrder(self.__instrument, -1 * positions[self.__instrument])

        elif bar.getPrice() > self.__sma[-1]:
            self.marketOrder(self.__instrument, 100)

        self._portfolioValues.append(self.getBroker().getEquity())


# Baixa os dados da ação
symbol = "PETR4"
interval = "1d"
period = "5y"
data = get_data_with_adj_close(symbol, interval, period)

# Salva os dados em formato CSV
data.to_csv(symbol + ".csv")

# Carrega os dados no PyAlgoTrade
feed = yahoofeed.Feed()
feed.addBarsFromCSV(symbol, symbol + ".csv")

# Configura o broker com um capital inicial
broker = backtesting.Broker(10000, feed)

# Executa a estratégia
myStrategy = MyStrategy(feed, symbol, 15)
myStrategy.run()


# Exibir resultados finais
print("Saldo final: $%.2f" % myStrategy.getBroker().getEquity())

# Gráfico de desempenho
plt.plot(myStrategy._portfolioValues)
plt.title('Performance da Carteira ao Longo do Tempo')
plt.xlabel('Barras')
plt.ylabel('Valor da Carteira')
plt.show()