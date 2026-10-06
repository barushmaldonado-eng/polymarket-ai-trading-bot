import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen

GAMMA_URL = "https://gamma-api.polymarket.com"
CLOB_URL = "https://clob.polymarket.com"

class PolymarketPublicData:
    def __init__(self, timeout=10):
        self.timeout = timeout

    def _get(self, base, path, params):
        url = base + path + "?" + urlencode(params)
        req = Request(url, headers={"User-Agent": "polymarket-ai-trading-bot/0.1"})
        with urlopen(req, timeout=self.timeout) as response:
            return json.loads(response.read().decode("utf-8"))

    def discover_markets(self, limit=100):
        data = self._get(GAMMA_URL, "/markets", {
            "active": "true", "closed": "false", "limit": limit
        })
        return data if isinstance(data, list) else data.get("data", [])

    @staticmethod
    def _token_ids(market):
        value = market.get("clobTokenIds") or market.get("clob_token_ids") or []
        if isinstance(value, str):
            try:
                value = json.loads(value)
            except json.JSONDecodeError:
                value = [value]
        return value

    def order_book(self, token_id):
        return self._get(CLOB_URL, "/book", {"token_id": token_id})

    @staticmethod
    def best_prices(book):
        bids = book.get("bids") or []
        asks = book.get("asks") or []
        bid = max((float(x["price"]) for x in bids), default=None)
        ask = min((float(x["price"]) for x in asks), default=None)
        return bid, ask

    def snapshots(self, limit=50):
        result = []
        for market in self.discover_markets(limit):
            tokens = self._token_ids(market)
            if not tokens:
                continue
            try:
                book = self.order_book(str(tokens[0]))
                bid, ask = self.best_prices(book)
            except Exception:
                continue
            result.append({
                "market_id": str(market.get("id") or market.get("conditionId") or ""),
                "question": market.get("question", ""),
                "token_id": str(tokens[0]),
                "best_bid": bid,
                "best_ask": ask,
                "spread": (ask - bid) if bid is not None and ask is not None else None,
            })
        return result
