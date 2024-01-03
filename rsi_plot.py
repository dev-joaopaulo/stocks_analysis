import matplotlib.pyplot as plt

def plot_rsi_data(historical_data, rsi, ticker, upper_threshold, lower_threshold):

    # Plotagem
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), gridspec_kw={'height_ratios': [3, 1]})

    # Gráfico de preço de fechamento
    ax1.plot(historical_data['Close'], label='Preço de Fechamento')
    ax1.set_title(f'Preço de Fechamento e RSI - {ticker}')
    ax1.set_ylabel('Preço de Fechamento')
    ax1.grid(True)
    ax1.legend()

    # Gráfico de RSI
    ax2.plot(rsi, label='RSI', color='orange')
    ax2.axhline(upper_threshold, color='red', linestyle='--')
    ax2.axhline(lower_threshold, color='green', linestyle='--')
    ax2.set_ylabel('RSI')
    ax2.set_xlabel('Data')
    ax2.grid(True)
    ax2.legend()

    plt.tight_layout()
    plt.show()