# Polymarket AI Trading Bot

Autonomous Polymarket trading framework with a conservative $50 bankroll profile.

## Safety state
The default mode is paper trading. Live trading requires BOT_MODE=live and ENABLE_LIVE_TRADING=1 plus runtime wallet credentials. Secrets are never committed.

## Strategy
The first live-capable strategy is narrow structural arbitrage for binary markets: buy YES and NO only when their executable ask prices sum below 1 by a configurable safety margin. This is not guaranteed risk-free because fills, liquidity, fees and settlement can change.

The scanner checks liquid order-book markets, both outcomes, minimum order size and executable prices. Live orders use FOK and explicit price limits. If the first leg succeeds and the second leg fails, the bot halts instead of silently carrying a new position.

## Risk defaults
- Bankroll: $50
- Max single leg: $2.50
- Max bundle exposure: $5
- Max daily loss: $2.50
- Max 5 live trades/day
- 60-second cooldown
- No martingale or automatic averaging down
- Fail closed on critical API/geoblock errors

## Runtime
Python 3.11+ and the official `polymarket-client` SDK.

Paper scan: `python scripts/paper_scan.py`

Long-running bot: `python -m bot.main`

Docker: `docker compose up -d --build`

Before live deployment, confirm Polymarket permits order placement from the server's network/location. Do not use a VPN to bypass restrictions.
