from cryptobacktest import cryptobacktest
from src.cryptobacktest import Option  # Adjust the import based on your file structure

def test_black_scholes():
    # Create an instance of the Option class
    option = Option(
        option_type="Call",
        underlying_price=100,  # Example underlying price
        strike_price=110,  # Example strike price
        interest_rate=0.05,  # Example risk-free interest rate (5%)
        dividend_yield=0.02,  # Example continuous dividend yield (2%)
        time_to_maturity=30,  # Example time to maturity in days
        implied_volatility=0.2  # Example implied volatility (20%)
    )

    # Call the black_scholes function
    bs_price = option.black_scholes()

    print("Black-Scholes Price:", bs_price)

if __name__ == "__main__":
    test_black_scholes()
