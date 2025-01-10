import pandas as pd
import numpy as np

class StrictVolatilitySignal:
    def __init__(self, vol_column: str, date_column: str, short_window: int, long_window: int, 
                 threshold_factor: float = 0.8, min_days: int = 5, trading_frequency: int = 30):
        """
        Initializes the StrictVolatilitySignal class.

        :param vol_column: Column name for the volatility data.
        :param date_column: Column name for the dates.
        :param short_window: Rolling window for short-term volatility (in days).
        :param long_window: Rolling window for long-term volatility (in days).
        :param threshold_factor: Factor to multiply the long-term volatility to define a threshold.
        :param min_days: Minimum consecutive days required to trigger a signal.
        :param trading_frequency: Minimum delay between two consecutive signals (in days).
        """
        self.vol_column = vol_column
        self.date_column = date_column
        self.short_window = short_window
        self.long_window = long_window
        self.threshold_factor = threshold_factor
        self.min_days = min_days
        self.trading_frequency = trading_frequency

    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Generate low volatility signals based on the rules the user decides.

        :param df: dff containing at least the volatility and date columns.
        :return DataFrame with an additional 'Signal' column.
        """
        df = df.copy()

        # Compute short-term and long-term rolling volatility
        df['ShortVol'] = df[self.vol_column].rolling(window=self.short_window).mean()
        df['LongVol'] = df[self.vol_column].rolling(window=self.long_window).mean()

        # Define the threshold based on the long-term volatility
        df['Threshold'] = df['LongVol'] * self.threshold_factor

        # Identify periods where short-term volatility is below the threshold
        df['BelowThreshold'] = (df['ShortVol'] < df['Threshold']).astype(int)

        # Identify consecutive days below the threshold
        df['ConsecutiveBelow'] = df['BelowThreshold'] * (df['BelowThreshold'].groupby((df['BelowThreshold'] != df['BelowThreshold'].shift()).cumsum()).cumcount() + 1)

        # Generate a signal only if the minimum number of days is verified.
        df['Signal'] = 0
        last_signal_date = None

        for idx, row in df.iterrows():
            current_date = row[self.date_column]
            if row['ConsecutiveBelow'] >= self.min_days:
                # Check trading frequency
                if last_signal_date is None or (current_date - last_signal_date).days >= self.trading_frequency:
                    df.at[idx, 'Signal'] = 1
                    last_signal_date = current_date

        # Drop intermediate columns if desired
        df = df.drop(columns=['ShortVol', 'LongVol', 'Threshold', 'BelowThreshold', 'ConsecutiveBelow'])
        return df