from dataclasses import dataclass
@dataclass
class MarketSnapshot:
    market_id: str
    question: str
    yes_price: float
    estimated_probability: float
    liquidity: float
class EdgeStrategy:
    def __init__(self, min_edge): self.min_edge = min_edge
    def evaluate(self, market):
        edge = market.estimated_probability - market.yes_price
        if edge >= self.min_edge: return {'side':'YES','edge':edge}
        return None
