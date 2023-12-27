from scipy.signal import find_peaks
import numpy as np


def calculate_rsi(historical_data, period=9):
    delta = historical_data['Adj Close'].diff()

    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    # Usa EMA ao invés de média móvel simples
    average_gain = gain.ewm(alpha=1/period, min_periods=period).mean()
    average_loss = loss.ewm(alpha=1/period, min_periods=period).mean()

    rs = average_gain / average_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi


def get_rsi_threshold(rsi, limit):
    return rsi.quantile(limit)


def get_upper_threshold_rsi(rsi, limit=90):
    return get_rsi_threshold(rsi, limit)


def get_lower_threshold_rsi(rsi, limit=10):
    return get_rsi_threshold(rsi, limit)


def get_average_lows_distance_by_period(rsi, min_distance=4):
    minima_indices = find_peaks(-rsi, distance=min_distance)[0]
    intervals = np.diff(minima_indices)
    average_interval = np.mean(intervals) if len(intervals) > 0 else np.nan
    return average_interval

