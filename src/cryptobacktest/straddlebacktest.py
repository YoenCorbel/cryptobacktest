from cryptobacktest.straddlebroker import StraddleBroker
import pandas as pd
from datetime import timedelta

class StraddleBacktest:
    def __init__(self, initial_date, final_date, data_module, initial_cash, allocation_percent=0.1):
        """
        Initializes the backtest.
        - initial_date: Start date of the backtest
        - final_date: End date of the backtest
        - data_module: Data module containing the input data
        - initial_cash: Starting cash for the portfolio
        - allocation_percent: Percentage of the portfolio to allocate for each straddle (sort of quantity)
        """
        self.initial_date = initial_date
        self.final_date = final_date
        self.data_module = data_module
        self.broker = StraddleBroker(initial_cash)  # Initialize the broker with starting cash
        self.allocation_percent = allocation_percent  # % of portfolio allocated to each straddle
        self.information = None  # To store the signal and pricing information

    def run_backtest(self, information_class):
        """
        Runs the backtest by iterating through the dates and processing signals (1 for buy, 0 for nothing).
        
        nformation_class: Class that computes signals and straddle prices.
        """
        self.information = information_class

        # Iterate through each date in the backtest range
        for current_date in pd.date_range(self.initial_date, self.final_date, freq="D"):
            info = self.information.compute_information(current_date)
            print(f"Processing date: {current_date}, Signal: {info['signal']}")  # allows easier debugging if needed

            # Extract spot prices for P&L calculations
            spot_prices = self.data_module.data.set_index("Date")["Close"].to_dict()

            # If signal, try to buy straddles
            if info["signal"] == 1 and info["straddle_price"] is not None:
                maturity_date = current_date + timedelta(days=30)  # Set a 30-day maturity in our case
                try:
                    self.broker.buy_straddles(
                        price=info["straddle_price"],
                        date=current_date,
                        maturity_date=maturity_date,
                        strike_price=spot_prices.get(current_date),
                        allocation_percent=self.allocation_percent,
                    )
                except ValueError as e:
                    print(f"Trade skipped on {current_date}: {e}")  # Log insufficient cash
                    # Append zero P&L for skipped trade
                    self.broker.realized_pnl.append(0.0)

            # Close any positions that have reached their maturity
            self.broker.close_expired_positions(current_date, spot_prices)

            # Log the portfolio's value and cash position for the current date
            current_spot = spot_prices.get(current_date, 0)
            self.broker.portfolio_value.append(
                {
                    "Date": current_date,
                    "PortfolioValue": self.broker.get_portfolio_value(current_spot),
                    "Cash": self.broker.cash,
                    "OpenPositions": len(self.broker.positions),
                }
            )

    def get_results(self):
        """
        Returns the results of the backtest: portfolio history and realized P&L.
        
        Returns:
        - portfolio_value: df of the portfolio's value over time.
        - realized_pnl: listt of realized P&L values.
        """
        return pd.DataFrame(self.broker.portfolio_value), self.broker.realized_pnl
