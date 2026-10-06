import os
from dataclasses import dataclass
from dotenv import load_dotenv
load_dotenv()
def money(name, default):
    return float(os.getenv(name, default))
@dataclass(frozen=True)
class Config:
    mode: str = os.getenv('BOT_MODE', 'paper')
    bankroll: float = money('BANKROLL_USD', 50)
    max_position: float = money('MAX_POSITION_USD', 5)
    max_exposure: float = money('MAX_TOTAL_EXPOSURE_USD', 10)
    max_daily_loss: float = money('MAX_DAILY_LOSS_USD', 2.5)
    min_edge: float = money('MIN_EDGE', 0.05)
    min_liquidity: float = money('MIN_LIQUIDITY_USD', 25)
    scan_interval: int = int(os.getenv('SCAN_INTERVAL_SECONDS', 30))
    def validate(self):
        if self.mode not in {'paper', 'live'}: raise ValueError('BOT_MODE must be paper or live')
        if self.bankroll <= 0: raise ValueError('BANKROLL_USD must be positive')
        if not 0 < self.max_position <= self.bankroll: raise ValueError('Invalid max position')
        if self.max_exposure < self.max_position: raise ValueError('Exposure must be >= position')
        if self.max_daily_loss <= 0: raise ValueError('Daily loss must be positive')
