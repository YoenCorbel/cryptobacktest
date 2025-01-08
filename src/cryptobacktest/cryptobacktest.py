import math
from typing import Callable, Dict
from typing import List, Tuple, Optional

import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.stats import norm



class Option:
    """
    A class to represent an option and perform various option pricing and Greek calculations
    using the Black-Scholes model.
    """
    DAYS_IN_YEAR = 365

    def __init__(self, option_type: str, underlying_price: float, strike_price: float, interest_rate: float,
                 dividend_yield: float, time_to_maturity: int, implied_volatility: float):
        """
        Initializes the Option.

        :param option_type: Type of the option 'Call' or 'Put'.
        :param underlying_price: Current price of the underlying asset.
        :param strike_price: Strike price of the option.
        :param interest_rate: Risk-free interest rate.
        :param dividend_yield: Continuous dividend yield of the underlying asset.
        :param time_to_maturity: Time to maturity in days.
        :param implied_volatility: Implied volatility of the underlying asset.
        """
        if option_type not in ["Call", "Put"]:
            raise ValueError("option_type must be 'Call' or 'Put'")
        if underlying_price <= 0 or strike_price <= 0 or time_to_maturity <= 0 or implied_volatility <= 0:
            raise ValueError(
                "Underlying Price, strike price, implied volatility and time to maturity must be positive values")
        
        self.option_type = option_type
        self.underlying_price = underlying_price
        self.strike_price = strike_price
        self.interest_rate = interest_rate
        self.dividend_yield = dividend_yield
        self.time_to_maturity = time_to_maturity
        self.implied_volatility = implied_volatility

    @staticmethod
    def norm_dist(d: float) -> float:
        """
        Standard normal cumulative distribution function.

        :param d: Input value.
        :return: Cumulative probability.
        """
        return norm.cdf(d)

    @staticmethod
    def normal_pdf(d: float) -> float:
        """
        Standard normal probability density function.

        :param d: Input value.
        :return: Density value.
        """
        return math.exp(-d ** 2 / 2) / math.sqrt(2 * math.pi)

    def _calculate_d1_d2(self, S: float, K: float, T: float, r: float, q: float, sigma: float) -> Tuple[float, float]:
        """
        Calculates d1 and d2 for the Black-Scholes formula.

        :param S: Current price of the underlying asset.
        :param K: Strike price of the option.
        :param T: Time to maturity in years.
        :param r: Risk-free interest rate.
        :param q: Continuous dividend yield of the underlying asset.
        :param sigma: Implied volatility of the underlying asset.
        :return: Tuple containing d1 and d2.
        """
        D1 = (
                (math.log(S * math.exp(-q * T) / (K * math.exp(-r * T))) +
                 0.5 * sigma ** 2 * T) /
                (sigma * math.sqrt(T))
        )
        D2 = D1 - sigma * math.sqrt(T)
        return D1, D2

    def black_scholes(self, underlying_price: Optional[float] = None, time_to_maturity: Optional[int] = None,
                      implied_volatility: Optional[float] = None) -> float:
        """
        Calculates the Black-Scholes price of an option.

        :param underlying_price: Current price of the underlying asset. Defaults to the initialized price.
        :param time_to_maturity: Time to maturity in days. Defaults to the initialized value.
        :param implied_volatility: Implied volatility of the underlying asset. Defaults to the initialized value.
        :return: Black-Scholes price of the option.
        """
        T = self.time_to_maturity / self.DAYS_IN_YEAR if time_to_maturity is None else time_to_maturity / self.DAYS_IN_YEAR
        S = self.underlying_price if underlying_price is None else underlying_price
        K = self.strike_price
        r = self.interest_rate
        q = self.dividend_yield
        sigma = self.implied_volatility if implied_volatility is None else implied_volatility

        D1, D2 = self._calculate_d1_d2(S, K, T, r, q, sigma)

        if self.option_type == "Call":
            return (S * math.exp(-q * T) * self.norm_dist(D1) -
                    K * math.exp(-r * T) * self.norm_dist(D2))
        else:
            return (K * math.exp(-r * T) * self.norm_dist(-D2) -
                    S * math.exp(-q * T) * self.norm_dist(-D1))

    ########### Greek Calculations
    def delta(self, underlying_price: Optional[float] = None, time_to_maturity: Optional[int] = None,
              implied_volatility: Optional[float] = None) -> float:
        """
        Calculates the Delta of an option.

        :param underlying_price: Current price of the underlying asset. Defaults to the initialized price.
        :param time_to_maturity: Time to maturity in days. Defaults to the initialized value.
        :param implied_volatility: Implied volatility of the underlying asset. Defaults to the initialized value.
        :return: Delta of the option.
        """
        T = self.time_to_maturity / self.DAYS_IN_YEAR if time_to_maturity is None else time_to_maturity / self.DAYS_IN_YEAR
        S = self.underlying_price if underlying_price is None else underlying_price
        K = self.strike_price
        r = self.interest_rate
        q = self.dividend_yield
        sigma = self.implied_volatility if implied_volatility is None else implied_volatility

        D1, _ = self._calculate_d1_d2(S, K, T, r, q, sigma)

        if self.option_type == "Call":
            return math.exp(-q * T) * self.norm_dist(D1)
        else:
            return math.exp(-q * T) * (self.norm_dist(D1) - 1)


    def vega(self, underlying_price: Optional[float] = None, time_to_maturity: Optional[int] = None,
             implied_volatility: Optional[float] = None) -> float:
        """
        Calculates the Vega of an option.
        Change in Option Price for a +1% increase in implied volatility.

        :param underlying_price: Current price of the underlying asset. Defaults to the initialized price.
        :param time_to_maturity: Time to maturity in days. Defaults to the initialized value.
        :param implied_volatility: Implied volatility of the underlying asset. Defaults to the initialized value.
        :return: Vega of the option.
        """
        T = self.time_to_maturity / self.DAYS_IN_YEAR if time_to_maturity is None else time_to_maturity / self.DAYS_IN_YEAR
        S = self.underlying_price if underlying_price is None else underlying_price
        K = self.strike_price
        r = self.interest_rate
        q = self.dividend_yield
        sigma = self.implied_volatility if implied_volatility is None else implied_volatility

        D1, _ = self._calculate_d1_d2(S, K, T, r, q, sigma)

        return (S * math.exp(-q * T) * self.normal_pdf(D1) * math.sqrt(T) * 0.01)

    def gamma(self, underlying_price: Optional[float] = None, time_to_maturity: Optional[int] = None,
              implied_volatility: Optional[float] = None) -> float:
        """
        Calculates the Gamma of an option.
        Variation of Option Price for ΔS=1

        :param underlying_price: Current price of the underlying asset. Defaults to the initialized price.
        :param time_to_maturity: Time to maturity in days. Defaults to the initialized value.
        :param implied_volatility: Implied volatility of the underlying asset. Defaults to the initialized value.
        :return: Gamma of the option.
        """
        T = self.time_to_maturity / self.DAYS_IN_YEAR if time_to_maturity is None else time_to_maturity / self.DAYS_IN_YEAR
        S = self.underlying_price if underlying_price is None else underlying_price
        K = self.strike_price
        r = self.interest_rate
        q = self.dividend_yield
        sigma = self.implied_volatility if implied_volatility is None else implied_volatility

        D1, _ = self._calculate_d1_d2(S, K, T, r, q, sigma)

        return (self.normal_pdf(D1) * math.exp(-q * T) / (S * sigma * math.sqrt(T)))
    

    def theta(self, underlying_price: Optional[float] = None, time_to_maturity: Optional[int] = None,
              implied_volatility: Optional[float] = None) -> float:
        """
        Calculates the Theta of an option.
        Change in Option Price due to the passage of 1 calendar day.

        :param underlying_price: Current price of the underlying asset. Defaults to the initialized price.
        :param time_to_maturity: Time to maturity in days. Defaults to the initialized value.
        :param implied_volatility: Implied volatility of the underlying asset. Defaults to the initialized value.
        :return: Theta of the option.
        """
        T = self.time_to_maturity / self.DAYS_IN_YEAR if time_to_maturity is None else time_to_maturity / self.DAYS_IN_YEAR
        S = self.underlying_price if underlying_price is None else underlying_price
        K = self.strike_price
        r = self.interest_rate
        q = self.dividend_yield
        sigma = self.implied_volatility if implied_volatility is None else implied_volatility

        D1, D2 = self._calculate_d1_d2(S, K, T, r, q, sigma)

        if self.option_type == "Call":
            return (-S * self.normal_pdf(D1) * sigma * math.exp(-q * T) / (2 * math.sqrt(T)) +
                    q * S * self.norm_dist(D1) * math.exp(-q * T) -
                    r * K * math.exp(-r * T) * self.norm_dist(D2)) / self.DAYS_IN_YEAR
        else:
            return (-S * self.normal_pdf(D1) * sigma * math.exp(-q * T) / (2 * math.sqrt(T)) -
                    q * S * self.norm_dist(-D1) * math.exp(-q * T) +
                    r * K * math.exp(-r * T) * self.norm_dist(-D2)) / self.DAYS_IN_YEAR


class Forward:
    def __init__(self, underlying_price):
        """
        This class represents a forward contract.

        :param underlying_price: The current price of the underlying asset.

        """
        self.underlying_price = underlying_price


class Portfolio:
    def __init__(self, portfolio_value):
        """
        This class represents a portfolio containing multiple options and forward contracts.

        :param portfolio_value: The total value of the portfolio.
        """
        self.portfolio_value = portfolio_value
        self.options = []  # List to store options and their quantities
        self.forwards = []  # List to store forwards and their quantities

    def add_option(self, option, quantity, contract_size):
        """
        Add an option to the portfolio.

        :param option: The Option object to add.
        :param quantity: The quantity of this option.
        :param contract_size: The contract size of the option.
        """
        self.options.append({'option': option, 'quantity': quantity, 'contract_size': contract_size})

    def add_forward(self, forward, quantity, contract_size):
        """
        Adds a new forward contract to the existing list of forwards.

        :param forward: The forward contract to add.
        :param quantity: The quantity of the forward contract.
        :param contract_size: The contract size of the forward contract.
        """
        self.forwards.append({'forward': forward, 'quantity': quantity, 'contract_size': contract_size})

    def total_premium_amount(self):
        """
        Calculate the total amount of premium for the portfolio based on the value of each option

        :return: the total amount of premium.
        """
        total_value = 0
        for entry in self.options:
            option = entry['option']
            quantity = entry['quantity']
            contract_size = entry['contract_size']
            total_value += option.black_scholes() * quantity * contract_size

        return total_value


    def delta(self):
        """
        Calculate the total delta of the portfolio.
        Portfolio Delta exposure normalized versus a variation in % of underlying price

        :return: The total delta of the portfolio.
        """
        total_delta = 0

        for entry in self.options:
            option = entry['option']
            quantity = entry['quantity']
            contract_size = entry['contract_size']
            total_delta += option.delta() * quantity * contract_size * option.underlying_price / self.portfolio_value

        for entry in self.forwards:
            forward = entry['forward']
            quantity = entry['quantity']
            contract_size = entry['contract_size']
            total_delta += quantity * contract_size * forward.underlying_price / self.portfolio_value

        return total_delta

    def gamma(self):
        """
        Calculate the total gamma of the portfolio.
        Variation of Portfolio Delta exposure for a 1% underlying price variation

        :return: The total gamma of the portfolio.
        """
        total_gamma = 0
        for entry in self.options:
            option = entry['option']
            quantity = entry['quantity']
            contract_size = entry['contract_size']
            total_gamma += option.gamma() * quantity * contract_size * option.underlying_price ** 2 / 100 / self.portfolio_value

        return total_gamma

    def vega(self):
        """
        Calculate the total vega of the portfolio.
        in basis points

        :return: The total vega of the portfolio.
        """
        total_vega = 0
        for entry in self.options:
            option = entry['option']
            quantity = entry['quantity']
            contract_size = entry['contract_size']
            total_vega += option.vega() * quantity * contract_size * 10000 / self.portfolio_value

        return total_vega

    def theta(self):
        """
        Calculate the total theta of the portfolio.
        in basis points

        :return: The total theta of the portfolio.
        """
        total_theta = 0
        for entry in self.options:
            option = entry['option']
            quantity = entry['quantity']
            contract_size = entry['contract_size']
            total_theta += option.theta() * quantity * contract_size * 10000 / self.portfolio_value

        return total_theta