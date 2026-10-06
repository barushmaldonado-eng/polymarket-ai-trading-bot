import time
from .config import Config
from .risk import RiskManager
from .strategy import ArbitrageStrategy
from .scanner import PolymarketScanner
from .storage import Storage
from .health import assert_trading_allowed
from .live import LiveTrader

def main():
    config=Config(); config.validate(); risk=RiskManager(config); storage=Storage(); scanner=PolymarketScanner(config.min_liquidity); strategy=ArbitrageStrategy(config.arbitrage_min_edge,config.arbitrage_max_bundle)
    live=None
    if config.mode=='live':
        assert_trading_allowed(); live=LiveTrader(config,risk,storage); print('LIVE MODE: strict limits active')
    else: print('PAPER MODE: no live orders will be submitted')
    while True:
        try:
            opportunities=scanner.scan(500); ranked=[]
            for market in opportunities:
                signal=strategy.evaluate(market)
                if signal: ranked.append(signal); storage.log_opportunity(signal)
            ranked.sort(key=lambda x:x['gross_edge'],reverse=True)
            if ranked:
                print('BEST SIGNAL',ranked[0])
                if live: live.maybe_execute(ranked[0])
            else: print('No qualifying signal.')
        except Exception as exc:
            storage.log_error(str(exc)); print('Loop error:',exc)
            if live: risk.state.halted=True
        time.sleep(config.scan_interval)
if __name__=='__main__': main()
