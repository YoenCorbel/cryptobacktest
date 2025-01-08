# read version from installed package
from importlib.metadata import version
__version__ = version("cryptobacktest")

# Import the Option class
from .cryptobacktest import Option
