from bot.scanner import PolymarketScanner
from bot.strategy import ArbitrageStrategy
from bot.storage import Storage

def main():
    scanner=PolymarketScanner(25)
    strategy=ArbitrageStrategy(0.05,4)
    rows=scanner.scan(100)
    storage=Storage()
    print("Scanned markets:", len(rows))
    signals=0
    for market in rows:
        signal=strategy.evaluate(market)
        if signal:
            signals += 1
            storage.log_opportunity(signal)
            print(signal)
    print("Qualifying paper signals:", signals)

if __name__=="__main__": main()
