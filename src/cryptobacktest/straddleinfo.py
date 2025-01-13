from pybacktestchain.data_module import Information
import pandas as pd

class StraddleInformation(Information):
    """
    Computes trading signals and straddle prices based on historical data while inheriting from Information class of pybaktestchain.
    """

    def __init__(self, data_module, s, time_column, adj_close_column):
        # Initialize the parent Information class with relevant parameters for our option strategy;
        super().__init__(s, data_module, time_column, None, adj_close_column) # Use super() to call the parent class's initializer for inherited attributes


    def compute_information(self, t: pd.Timestamp):
        """
        Calculates the signal and straddle price at a specific time.

        Args:
            t: Timestamp for which the signal and straddle price are computed.

        Returns:
            Returns the signal, straddle price, and the timestamp.
        """
        sliced_data = self.slice_data(t)  # Filter data within the lookback period
        sliced_data = sliced_data.sort_values(by=self.time_column)  # Sort by date

        latest_data = sliced_data.iloc[-1] if not sliced_data.empty else None
        signal = int(latest_data['Signal']) if latest_data is not None else 0
        straddle_price = latest_data['StraddlePrice'] if latest_data is not None else None

        return {"signal": signal, "straddle_price": straddle_price, "date": t}

    def slice_data(self, t: pd.Timestamp):
        """
        Extracts data from the lookback period ending at the given timestamp.

        Args:
            t: The end timestamp for the slicing window.

        Returns:
            Sliced data within the lookback window.
        """
        data = self.data_module.data
        s = self.s

        t = pd.Timestamp(t)
        #Manage potential timezone issues:
        if t.tzinfo is None:  # Handle timezone-naive timestamps
            data[self.time_column] = pd.to_datetime(data[self.time_column]).dt.tz_localize(None)
        else:  # Ensure timezone alignment for timezone-aware timestamps
            data[self.time_column] = pd.to_datetime(data[self.time_column]).apply(
                lambda x: x.tz_convert(t.tzinfo) if x.tzinfo else x.tz_localize(t.tzinfo)
            )

        # Return data within the lookback window
        return data[(data[self.time_column] >= t - s) & (data[self.time_column] < t)]
