def calculate_atr(data, periods):
    # Deslocar a coluna 'Close' para usar no cálculo do True Range
    previous_close = data['Close'].shift(1)

    # Calcular o True Range
    data['TR'] = data.apply(lambda x: max(x['High'] - x['Low'],
                                      abs(x['High'] - previous_close[x.name]),
                                      abs(x['Low'] - previous_close[x.name])), axis=1)

    data['ATR'] = data['TR'].rolling(window=periods).mean()
    return data

