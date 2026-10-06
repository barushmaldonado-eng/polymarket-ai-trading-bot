# Polymarket AI Trading Bot

SAFE MODE: PAPER TRADING ONLY.

Experimental automated trading system for Polymarket. Default bankroll is $50 with strict risk limits. No private keys or credentials belong in this repository.

Architecture: market data -> scanner -> strategy -> risk manager -> paper execution -> logs.

Run: `python -m bot.main`

This initial build deliberately disables live execution. Backtests and paper results do not guarantee future performance.
