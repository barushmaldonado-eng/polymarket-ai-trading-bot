from dataclasses import dataclass
from datetime import date
@dataclass
class RiskState:
    exposure: float=0.0
    realized_pnl_today: float=0.0
    trades_today: int=0
    halted: bool=False
    day: date=date.today()
class RiskManager:
    def __init__(self,config): self.config=config; self.state=RiskState()
    def _roll_day(self):
        today=date.today()
        if self.state.day!=today: self.state=RiskState(day=today)
    def approve(self,size,liquidity):
        self._roll_day()
        if self.state.halted: return False,'kill switch active'
        if self.state.trades_today>=self.config.max_trades_per_day: return False,'daily trade limit'
        if size<=0 or size>self.config.max_position: return False,'position limit'
        if self.state.exposure+size>self.config.max_exposure: return False,'total exposure limit'
        if liquidity<self.config.min_liquidity: return False,'insufficient liquidity'
        if self.state.realized_pnl_today<=-self.config.max_daily_loss: self.state.halted=True; return False,'daily loss limit'
        return True,'approved'
    def reserve(self,size): self.state.exposure+=size; self.state.trades_today+=1
    def release(self,size): self.state.exposure=max(0.0,self.state.exposure-size)
    def record_close(self,pnl):
        self._roll_day(); self.state.realized_pnl_today+=pnl
        if self.state.realized_pnl_today<=-self.config.max_daily_loss: self.state.halted=True
