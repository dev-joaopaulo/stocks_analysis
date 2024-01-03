import math


def get_unit_risk(entry, stop):
    return entry - stop


def get_number_stocks_based_on_risk(unit_risk, max_risk):
    return math.ceil(max_risk / unit_risk)


def get_risk_target_based_on_number_stocks(unit_risk, num_stocks, profit_target):
    return profit_target/(unit_risk * num_stocks)