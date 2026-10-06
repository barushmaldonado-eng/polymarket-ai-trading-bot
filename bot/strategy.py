from dataclasses import dataclass
@dataclass(frozen=True)
class MarketSnapshot:
    market_id:str
    question:str
    yes_asset:str
    no_asset:str
    yes_ask:float
    no_ask:float
    yes_size:float
    no_size:float
    minimum_order_size:float
    @property
    def gross_edge(self): return 1.0-self.yes_ask-self.no_ask
    @property
    def pair_cost(self): return self.yes_ask+self.no_ask
    @property
    def best_pair_shares(self): return min(self.yes_size,self.no_size)
class ArbitrageStrategy:
    def __init__(self,min_edge,max_bundle_usd): self.min_edge=min_edge; self.max_bundle_usd=max_bundle_usd
    def evaluate(self,m):
        if m.yes_ask<=0 or m.no_ask<=0 or m.pair_cost>=1.0-self.min_edge: return None
        shares=min(m.best_pair_shares,self.max_bundle_usd/m.pair_cost)
        if shares<m.minimum_order_size: return None
        yes_spend=shares*m.yes_ask; no_spend=shares*m.no_ask
        return {'market_id':m.market_id,'question':m.question,'yes_asset':m.yes_asset,'no_asset':m.no_asset,'shares':shares,'yes_spend':yes_spend,'no_spend':no_spend,'bundle_spend':yes_spend+no_spend,'gross_edge':m.gross_edge,'yes_max_price':m.yes_ask,'no_max_price':m.no_ask}
