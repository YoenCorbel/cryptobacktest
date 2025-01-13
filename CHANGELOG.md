# CHANGELOG


## v1.4.0 (2025-01-13)

### Features

- **package**: A class that inherits from pybackteschain information class but adapted to our option
  case.
  ([`7257283`](https://github.com/YoenCorbel/cryptobacktest/commit/7257283aa3fb672c2f756f12391747a3bb812936))

- **package**: A class that inherits from pybacktestchain brokerclass but adapted to our option case
  (no SL, no short positions, etc.)
  ([`f495e08`](https://github.com/YoenCorbel/cryptobacktest/commit/f495e088b02cc7c5b4d3521b569aae3e449cbe2d))

- **package**: A class to run a backtest, it doesn't inherit from pybacktest chain as it acts as a
  modular controller combining broker and information classes
  ([`1c43815`](https://github.com/YoenCorbel/cryptobacktest/commit/1c4381554acef9b5bf08cc21d218d24d3150c8be))

- **package**: Final version of the example; containing all necessary steps to run a backtest with
  the different developed functions
  ([`b22b84a`](https://github.com/YoenCorbel/cryptobacktest/commit/b22b84a674afe7fb2ae1afc6122ad4882b9a120e))

- **package**: Updated the README file with the potential continuations of the project if someone is
  interested.
  ([`0383439`](https://github.com/YoenCorbel/cryptobacktest/commit/0383439eebf087e280e060395577e8444f41d0bb))


## v1.3.0 (2025-01-10)

### Features

- **package**: Added a volatilitysignal class to detect potential nteresting periods of low
  volatility compared to historical one, to buy a straddle
  ([`8e83e31`](https://github.com/YoenCorbel/cryptobacktest/commit/8e83e310d05cb1b0c8eaa8fc3f82f1e30a349f2e))

- **package**: Applied our signal class to our jupyter example
  ([`7203b77`](https://github.com/YoenCorbel/cryptobacktest/commit/7203b77be81b412174d1a0a4fcdea10dd81f4068))


## v1.2.0 (2025-01-10)

### Build System

- Add PSR as dev dependency
  ([`3173096`](https://github.com/YoenCorbel/cryptobacktest/commit/31730965308cda23b21d6310abccf6c04d7dcbad))

### Features

- **package**: Added a volatility class to compute historical volatility as a proxy for option
  pricing implied volatility
  ([`8e1aa66`](https://github.com/YoenCorbel/cryptobacktest/commit/8e1aa6633da3553a583bc2e879dcc7a65519277f))

- **package**: Continued the jupyter example with the next impleme
  ([`72bde3a`](https://github.com/YoenCorbel/cryptobacktest/commit/72bde3ab4c8db50310498f97f241060bd51b87b0))

- **package**: Defined more clearly my option class and added a fu
  ([`994ea28`](https://github.com/YoenCorbel/cryptobacktest/commit/994ea28438869613eaea3b4dddd6461952255101))


## v1.1.0 (2025-01-10)

### Features

- Added a jupyter notebook to create an example usage of my library
  ([`834371c`](https://github.com/YoenCorbel/cryptobacktest/commit/834371c719e654c28b06f725ffc20cb881664640))


## v1.0.0 (2025-01-08)

### Features

- Trigger major version bump - <Implemented an Option class to compute the greeks and a portfolio
  class to aggregate risks of option strategies>
  ([`cc5a5fd`](https://github.com/YoenCorbel/cryptobacktest/commit/cc5a5fd7fc532b74168376faaa9696d3ecb47d5b))
