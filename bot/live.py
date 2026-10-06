from polymarket import SecureClient
from .risk import RiskManager
from .storage import Storage

class LiveTrader:
    def __init__(self,config,risk: RiskManager,storage: Storage):
        self.config=config
        self.risk=risk
        self.storage=storage
        self.client=SecureClient.create(
            private_key=config.private_key,
            wallet=config.wallet or None,
        )

    def maybe_execute(self,signal):
        bundle=float(signal['bundle_spend'])
        if bundle>self.config.max_exposure:
            return {'status':'rejected','reason':'bundle exposure'}
        if signal['yes_spend']>self.config.max_position or signal['no_spend']>self.config.max_position:
            return {'status':'rejected','reason':'leg exposure'}
        best_liquidity=min(float(signal['yes_spend']),float(signal['no_spend']))
        ok,reason=self.risk.approve(max(float(signal['yes_spend']),float(signal['no_spend'])),best_liquidity)
        if not ok:
            self.storage.log_trade({'status':'rejected','reason':reason,**signal})
            return {'status':'rejected','reason':reason}
        reserved=False
        try:
            self.risk.reserve(bundle)
            reserved=True
            yes=self.client.place_market_order(
                asset_id=signal['yes_asset'],
                side='BUY',
                amount=signal['yes_spend'],
                max_price=signal['yes_max_price'],
                order_type='FOK',
            )
            if not getattr(yes,'ok',False):
                self.risk.release(bundle)
                reserved=False
                raise RuntimeError('YES leg rejected: '+str(yes))
            no=self.client.place_market_order(
                asset_id=signal['no_asset'],
                side='BUY',
                amount=signal['no_spend'],
                max_price=signal['no_max_price'],
                order_type='FOK',
            )
            if not getattr(no,'ok',False):
                self.risk.state.halted=True
                raise RuntimeError('NO leg rejected after YES fill; bot halted for manual reconciliation: '+str(no))
            payload={
                'status':'matched_pair',
                'yes_order_id':str(yes.order_id),
                'no_order_id':str(no.order_id),
                **signal,
            }
            self.storage.log_trade(payload)
            return payload
        except Exception as exc:
            self.storage.log_trade({'status':'ERROR_HALTED','error':str(exc),**signal})
            self.risk.state.halted=True
            raise

    def close(self):
        self.client.close()
