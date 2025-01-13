from pybacktestchain.broker import Broker
from dataclasses import dataclass
import pandas as pd


@dataclass
class Straddle:
    purchase_date: pd.Timestamp
    price: float
    maturity_date: pd.Timestamp
    strike_price: float
    quantity: int  # Quantity of straddles


class StraddleBroker(Broker):
    def __init__(self, cash: float):
        """
        Initializes the StraddleBroker with a starting cash balance and necessary attributes.
        """
        super().__init__(cash)  # Initialize with parent Broker class
        self.positions = []  # List of current straddle positions
        self.realized_pnl = []  # List of realized P&L
        self.portfolio_value = []  # Track portfolio value over time

    def buy_straddles(self, price, date, maturity_date, strike_price, allocation_percent):
        """
        Buys straddles based on the allocation percentage of the portfolio value.

            price: The price of a single straddle.
            date: The purchase date.
            maturity_date: The maturity date of the straddle.
            strike_price: The strike price of the straddle.
            allocation_percent: Percentage of portfolio allocated to buying straddles.
        """
        max_cash_to_allocate = self.cash * allocation_percent
        quantity = int(max_cash_to_allocate // price)  # Calculate the number of straddles to buy
        total_cost = quantity * price

        if total_cost <= self.cash and quantity > 0:
            self.cash -= total_cost #remove the paid premium
            self.positions.append(
                Straddle(
                    purchase_date=date,
                    price=price,
                    maturity_date=maturity_date,
                    strike_price=strike_price,
                    quantity=quantity,
                )
            )
            # Log the transaction with quantity, price, and total cost
            self.log_transaction(date, "BUY_STRADDLE", quantity, price, total_cost)
        else:
            raise ValueError("Not enough cash to buy straddles.")

    def close_expired_positions(self, current_date, spot_prices):
        """
        Closes all straddle positions that expire on or before the current date.

            current_date: The date on which to close expired positions.
            spot_prices: A dictionary of spot prices with dates as keys.
        """
        remaining_positions = []
        for pos in self.positions:
            if current_date >= pos.maturity_date:
                # Calculate the payoff at maturity
                maturity_spot = spot_prices.get(pos.maturity_date)
                if maturity_spot is not None:
                    call_payoff = max(maturity_spot - pos.strike_price, 0) #payoff call
                    put_payoff = max(pos.strike_price - maturity_spot, 0) #payoff put
                    payoff = (call_payoff + put_payoff) * pos.quantity #payoff straddle
                else:
                    payoff = 0  # Assume no payoff if maturity price is unavailable

                # Realized P&L
                pnl = payoff - (pos.price * pos.quantity)
                self.realized_pnl.append(pnl)
                self.cash += payoff  # Add payoff to cash

                # Log the transaction
                self.log_transaction(current_date, "CLOSE_STRADDLE", pos.quantity, pos.price, payoff)
            else:
                remaining_positions.append(pos)

        self.positions = remaining_positions  # Update remaining positions

    def get_portfolio_value(self, current_spot):
        """
        Calculate the current portfolio value, including cash and open positions.

        Args:
            current_spot (float): The current spot price of the asset.

        Returns:
            float: The total portfolio value.
        """
        value = self.cash
        for pos in self.positions:
            call_payoff = max(current_spot - pos.strike_price, 0)
            put_payoff = max(pos.strike_price - current_spot, 0)
            value += (call_payoff + put_payoff) * pos.quantity
        return value
