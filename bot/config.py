import os
from dataclasses import dataclass
from dotenv import load_dotenv
load_dotenv()

def money(name, default): return float(os.getenv(name, default))
def boolean(name, default=False):
    raw=os.getenv(name)
    return default if raw is None else raw.strip().lower() in {'1','true','yes','on'}

@dataclass(frozen=True)
class Config:
    mode: str = os.getenv('BOT_MODE','paper').strip().lower()
    bankroll: float = money('BANKROLL_USD',50)
    max_position: float = money('MAX_POSITION_USD',2.5)
    max_exposure: float = money('MAX_TOTAL_EXPOSURE_USD',5)
    max_daily_loss: float = money('MAX_DAILY_LOSS_USD',2.5)
    arbitrage_min_edge: float = money('ARBITRAGE_MIN_EDGE',0.05)
    arbitrage_max_bundle: float = money('ARBITRAGE_MAX_BUNDLE_USD',4)
    min_liquidity: float = money('MIN_LIQUIDITY_USD',25)
    scan_interval: int = int(os.getenv('SCAN_INTERVAL_SECONDS','10'))
    trade_cooldown: int = int(os.getenv('TRADE_COOLDOWN_SECONDS','60'))
    max_trades_per_day: int = int(os.getenv('MAX_TRADES_PER_DAY','5'))
    max_unwind_slippage: float = money('MAX_UNWIND_SLIPPAGE',0.15)
    enable_live_trading: bool = boolean('ENABLE_LIVE_TRADING',False)
    private_key: str = os.getenv('POLYMARKET_PRIVATE_KEY','')
    wallet: str = os.getenv('POLYMARKET_WALLET','')
    def validate(self):
        if self.mode not in {'paper','live'}: raise ValueError('BOT_MODE must be paper or live')
        if self.bankroll <= 0: raise ValueError('BANKROLL_USD must be positive')
        if not 0 < self.max_position <= self.bankroll: raise ValueError('Invalid max position')
        if self.max_exposure < self.max_position or self.max_exposure > self.bankroll: raise ValueError('Invalid exposure')
        if not 0 < self.max_daily_loss <= self.bankroll: raise ValueError('Invalid daily loss')
        if not 0 < self.arbitrage_min_edge < 1: raise ValueError('Invalid arbitrage edge')
        if self.arbitrage_max_bundle <= 0 or self.arbitrage_max_bundle > self.max_exposure: raise ValueError('Invalid bundle size')
        if self.scan_interval < 2: raise ValueError('SCAN_INTERVAL_SECONDS too small')
        if self.trade_cooldown < 0 or self.max_trades_per_day < 1: raise ValueError('Invalid trading limits')
        if self.mode == 'live' and not self.enable_live_trading: raise ValueError('Live mode requires ENABLE_LIVE_TRADING=1')
        if self.mode == 'live' and not self.private_key: raise ValueError('POLYMARKET_PRIVATE_KEY required for live mode')
