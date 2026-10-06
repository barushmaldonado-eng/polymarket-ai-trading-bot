import json, os
from datetime import datetime, timezone
class PaperExecutor:
    def __init__(self, config, risk): self.config, self.risk = config, risk; os.makedirs('logs', exist_ok=True)
    def execute(self, market_id, side, price, size, edge):
        ok, reason = self.risk.approve(size, self.config.min_liquidity)
        if not ok: return {'status':'rejected','reason':reason}
        self.risk.state.exposure += size
        event={'timestamp':datetime.now(timezone.utc).isoformat(),'mode':'paper','market_id':market_id,'side':side,'price':price,'size_usd':size,'edge':edge,'status':'simulated'}
        with open('logs/trades.jsonl','a',encoding='utf-8') as f: f.write(json.dumps(event)+'\n')
        return event
