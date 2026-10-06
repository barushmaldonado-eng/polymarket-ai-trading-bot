from polymarket import SecureClient
from .risk import RiskManager
from .storage import Storage

class LiveTrader:
    def __init__(self, config, risk: RiskManager, storage: Storage):
        if not config.private_key:
            raise RuntimeError("POLYMARKET_PRIVATE_KEY is required for live mode")
        self.config=config
        self.risk=risk
        self.storage=storage
        self.client=SecureClient.create(
            private_key=config.private_key,
            wallet=config.wallet or None,
        )

    def maybe_execute(self, signal):
        size=min(
            float(signal["shares"] * signal["yes_spend"] / signal["bundle_spend"]),
            self.config.max_position,
        )
        if signal["bundle_spend"] > self.config.max_exposure:
            return {"status":"rejected","reason":"bundle exceeds exposure"}
        ok, reason=self.risk.approve(size, self.config.min_liquidity)
        if not ok:
            self.storage.log_trade({"status":"rejected","reason":reason,**signal})
            return {"status":"rejected","reason":reason}

        # FOK + max_price/min_price constraints reduce unexpected execution.
        shares=float(signal["shares"])
        yes_spend=float(signal["yes_spend"])
        no_spend=float(signal["no_spend"])
        yes_price=float(signal["yes_spend"] / shares)
        no_price=float(signal["no_spend"] / shares)

        try:
            self.risk.reserve(float(signal["bundle_spend"]))
            yes=self.client.place_market_order(
                asset_id=signal["yes_asset"],
                side="BUY",
                amount=yes_spend,
                max_price=yes_price,
                order_type="FOK",
            )
            no=self.client.place_market_order(
                asset_id=signal["no_asset"],
                side="BUY",
                amount=no_spend,
                max_price=no_price,
                order_type="FOK",
            )
            payload={"status":"submitted","yes":str(yes),"no":str(no),**signal}
            self.storage.log_trade(payload)
            return payload
        except Exception as exc:
            self.risk.state.halted=True
            self.storage.log_trade({"status":"ERROR_AND_HALTED","error":str(exc),**signal})
            raise
        finally:
            self.client.close()
