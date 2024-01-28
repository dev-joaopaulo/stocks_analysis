from atr_indicator import calculate_atr


def get_simple_stop(data, index, row):
    # Determinar o stop como 0.01 abaixo do valor mínimo entre a semana identificada e a semana anterior
    previous_previous_week_low = data.iloc[data.index.get_loc(index) - 2]['Low']
    previous_week_low = data.iloc[data.index.get_loc(index) - 1]['Low']
    current_week_low = row['Low']
    stop = min(previous_week_low, current_week_low, previous_previous_week_low) - 0.01
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
    
