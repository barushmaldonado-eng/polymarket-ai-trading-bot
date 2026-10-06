# Live setup

This repository is ready for live execution, but credentials must be supplied outside Git.

## 1. Persistent Linux VPS

Install Docker, clone the repository, and create `.env` from `.env.example`.

Set:

```text
BOT_MODE=live
ENABLE_LIVE_TRADING=1
POLYMARKET_PRIVATE_KEY=<your wallet signing key>
POLYMARKET_WALLET=<the wallet/funder address, when required>
```

Never paste the private key into a GitHub file, issue, commit, chat, or screenshot.

## 2. Start

```bash
docker compose up -d --build
docker compose logs -f
```

The container is configured with restart: unless-stopped.

## 3. Safety profile

- $2.50 maximum per leg
- $5 maximum bundle exposure
- $2.50 maximum realized daily loss
- 5 live trades/day
- FOK orders only
- explicit buy-price caps
- no martingale
- critical errors activate the kill switch

## 4. Before funding

Run paper mode first:

```bash
docker compose run --rm bot python scripts/paper_scan.py
```

Only fund the account after confirming the scanner works in the target environment and that Polymarket permits order placement from that network/location.

A VPS is required for continuous 24/7 operation; GitHub is source control, not a permanent trading server.