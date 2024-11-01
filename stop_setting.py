from atr_indicator import calculate_atr


def get_simple_stop(data, index, row, num_periods):
    # Verificar se temos dados suficientes
    if data.index.get_loc(index) < num_periods:
        raise ValueError("Dados insuficientes para calcular o stop para o número de períodos fornecido.")
    
    # Calcular o stop baseado no número de períodos fornecido
    lows = [data.iloc[data.index.get_loc(index) - i]['Low'] for i in range(1, num_periods + 1)]
    current_week_low = row['Low']
    stop = min(lows + [current_week_low]) - 0.01
    
    return stop


def get_moving_stop_atr(week, current_stop, atr_factor):
    stop = current_stop
    if is_positive_week_close(week):
        moving_stop = get_stop_atr(week['Close'], week['ATR'], atr_factor)
        if moving_stop > current_stop:
            stop = moving_stop
    return stop
        

def get_stop_atr(price, atr, factor):
    return price - atr * factor


def current_stop_finder(data, current_stop, factor, atr_periods=20):
    data = calculate_atr(data, atr_periods)
    for i in reversed(data.index):
        week = data.loc[i]
        if is_positive_week_close(week):
            moving_stop = get_stop_atr(week['Close'], week['ATR'], factor)
            if moving_stop > current_stop:
                return moving_stop
            else:
                return current_stop
        
        
def is_positive_week_close(week):
    return week['Close'] > week['Open']
    
