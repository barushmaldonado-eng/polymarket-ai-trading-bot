from dataclasses import dataclass
@dataclass
class RiskState:
    exposure: float = 0.0
    realized_pnl_today: float = 0.0
    halted: bool = False
class RiskManager:
    def __init__(self, config): self.config, self.state = config, RiskState()
    def approve(self, size, liquidity):
        if self.state.halted: return False, 'kill switch active'
        if size <= 0 or size > self.config.max_position: return False, 'position limit'
        if self.state.exposure + size > self.config.max_exposure: return False, 'total exposure limit'
        if liquidity < self.config.min_liquidity: return False, 'insufficient liquidity'
        if self.state.realized_pnl_today <= -self.config.max_daily_loss:
            self.state.halted = True; return False, 'daily loss limit'
        return True, 'approved'
    def record_close(self, pnl):
        self.state.realized_pnl_today += pnl
        if self.state.realized_pnl_today <= -self.config.max_daily_loss: self.state.halted = True
