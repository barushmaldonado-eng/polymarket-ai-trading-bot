"""Polymarket integration boundary. No credentials or live order submission."""
class PolymarketAdapter:
    def fetch_markets(self): raise NotImplementedError('Market-data adapter not configured yet.')
    def submit_order(self,*args,**kwargs): raise NotImplementedError('Live order submission is intentionally disabled.')
