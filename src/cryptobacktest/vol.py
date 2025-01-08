import pandas as pd
import numpy as np

class Volatility:
    """
    A class to compute rolling volatilities and aggregate them by month.
    """

    def __init__(self, historical_prices: pd.Series):
        """
        Initialize the Volatility class with historical price data.

        :param historical_prices: A pandas Series of historical prices indexed by date.
        """
        self.historical_prices = historical_prices.sort_index()

    def compute_monthly_30d_volatility(self) -> pd.Series:
        """
        Compute the 30-day rolling annualized volatility for each month.

        :return: A pandas Series with the 30-day volatility aggregated by month.
        """
        # Calculate daily returns
        daily_returns = self.historical_prices.pct_change().dropna()

        # Calculate rolling 30-day volatility
        rolling_volatility = (
            daily_returns.rolling(window=30).std() * np.sqrt(252)
        )

        # Resample by month and take the last value of rolling volatility for each month
        monthly_volatility = rolling_volatility.resample('M').last()

        return monthly_volatility
