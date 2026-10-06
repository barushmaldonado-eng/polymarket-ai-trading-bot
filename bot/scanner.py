from decimal import Decimal
from polymarket import PublicClient
from .strategy import MarketSnapshot

class PolymarketScanner:
    def __init__(self, min_liquidity: float):
        self.min_liquidity = Decimal(str(min_liquidity))

    def scan(self, limit: int = 500):
        found = []
        with PublicClient() as client:
            page = client.list_markets(
                closed=False,
                page_size=min(limit, 1000),
                order="liquidityNum",
                ascending=False,
            ).first_page()
            for market in page.items:
                if market.state.enable_order_book is not True or market.state.accepting_orders is not True:
                    continue
                yes = market.outcomes.yes
                no = market.outcomes.no
                yes_id = yes.token_id or yes.position_id
                no_id = no.token_id or no.position_id
                if not yes_id or not no_id:
                    continue
                try:
                    yb = client.get_order_book(asset_id=yes_id)
                    nb = client.get_order_book(asset_id=no_id)
                except Exception:
                    continue
                if not yb.asks or not nb.asks:
                    continue
                ya, na = yb.asks[-1], nb.asks[-1]
                if ya.size <= 0 or na.size <= 0:
                    continue
                liquidity = float(min(ya.size * ya.price, na.size * na.price))
                if liquidity < float(self.min_liquidity):
                    continue
                found.append(MarketSnapshot(
                    market_id=str(market.id),
                    question=market.question or market.slug or str(market.id),
                    yes_asset=str(yes_id),
                    no_asset=str(no_id),
                    yes_ask=float(ya.price),
                    no_ask=float(na.price),
                    yes_size=float(ya.size),
                    no_size=float(na.size),
                    minimum_order_size=float(yb.min_order_size),
                ))
        return found
