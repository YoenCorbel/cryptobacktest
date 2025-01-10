import pandas as pd
import numpy as np
import math
import yfinance as yf
import datetime
import matplotlib.pyplot as plt

class Volatility:
    """
    A class to compute rolling volatilities for cryptocurrencies.
    """

    def __init__(self, window: int = 360, factor: int = 360):
        """
        Initialize the Volatility class.

        :param window: The rolling window size (e.g., 30 days for a month).
        :param factor: The factor to multiply daily volatility (default is 360 for yearly vol)

        """
        self.window = window
        self.factor = factor


    def compute_volatility(self, df: pd.DataFrame, price_column: str, date_column: str = None) -> pd.DataFrame:
        """
        Compute rolling monthly volatility for cryptocurrencies.

        :param df: The input DataFrame with price data.
        :param price_column: The name of the column containing prices.
        :param date_column: The name of the date column (optional, ensures sorting by date).
        :return: The original DataFrame with an added 'Volatility' column.
        """
        # Ensure the DataFrame is sorted by date if a date column is provided
        if date_column:
            df = df.sort_values(by=date_column)

        # Calculate daily returns
        df['Returns'] = df[price_column].pct_change()

        # Calculate rolling monthly volatility
        df['Volatility'] = df['Returns'].rolling(window=self.window).std()*np.sqrt(self.factor)

        # Drop the 'Returns' column as it's intermediate
        df.drop(columns=['Returns'], inplace=True)

        return df
