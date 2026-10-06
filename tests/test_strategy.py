from bot.strategy import ArbitrageStrategy, MarketSnapshot

def market(yes, no):
    return MarketSnapshot("1","test","yes","no",yes,no,100,100,1)

def test_detects_edge():
    s=ArbitrageStrategy(0.05,4)
    x=s.evaluate(market(0.45,0.45))
    assert x is not None
    assert x["gross_edge"] == 0.10

def test_rejects_small_edge():
    s=ArbitrageStrategy(0.05,4)
    assert s.evaluate(market(0.48,0.50)) is None
