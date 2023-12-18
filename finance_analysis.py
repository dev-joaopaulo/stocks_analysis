def get_annualized_return(period, profit):
    """
    Calculate the annualized return of an investment.

    Parameters:
    period (int): The number of days the investment was held.
    profit (float): The profit or loss from the investment.

    Returns:
    float: The annualized return of the investment.
    """

    # Checking for zero or negative period
    if period <= 0:
        raise ValueError("The period must be a positive integer.")

    # Calculating the annualized return
    annualized_return = ((1 + profit) ** (365 / period)) - 1

    return annualized_return
