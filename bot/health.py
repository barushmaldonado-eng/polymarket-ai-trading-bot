import os
from urllib.request import Request, urlopen

def assert_trading_allowed():
    # Polymarket exposes a public geoblock endpoint. We fail closed if the
    # endpoint is unreachable instead of guessing whether trading is allowed.
    req=Request("https://polymarket.com/api/geoblock", headers={"User-Agent":"polymarket-ai-trading-bot/0.1"})
    with urlopen(req, timeout=10) as response:
        if response.status != 200:
            raise RuntimeError("Could not verify Polymarket geoblock status")
        data=response.read().decode("utf-8").lower()
    if "blocked" in data and ("true" in data or '"blocked":true' in data):
        raise RuntimeError("Polymarket reports this location/network as blocked")
