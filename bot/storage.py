import json, os
from datetime import datetime, timezone

class Storage:
    def __init__(self):
        os.makedirs("logs", exist_ok=True)

    def _write(self, filename, payload):
        with open(os.path.join("logs", filename), "a", encoding="utf-8") as f:
            f.write(json.dumps(payload, default=str) + "\n")

    def log_opportunity(self, signal):
        self._write("opportunities.jsonl", {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            **signal,
        })

    def log_trade(self, payload):
        self._write("trades.jsonl", {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            **payload,
        })

    def log_error(self, error):
        self._write("errors.jsonl", {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "error": error,
        })
