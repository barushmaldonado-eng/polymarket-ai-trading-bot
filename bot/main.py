import time
from .config import Config
from .risk import RiskManager
from .strategy import EdgeStrategy, MarketSnapshot
from .paper import PaperExecutor
def demo_market():
    return MarketSnapshot('demo','Demo market',0.45,0.52,100)
def main():
    config=Config(); config.validate()
    if config.mode == 'live': raise RuntimeError('Live execution is disabled in this initial build.')
    risk=RiskManager(config); strategy=EdgeStrategy(config.min_edge); executor=PaperExecutor(config,risk)
    print('Bot started in PAPER mode with bankroll $%.2f' % config.bankroll)
    while True:
        market=demo_market(); signal=strategy.evaluate(market)
        if signal: print(executor.execute(market.market_id,signal['side'],market.yes_price,min(config.max_position,2.0),signal['edge']))
        else: print('No qualifying signal.')
        time.sleep(config.scan_interval)
if __name__ == '__main__': main()
