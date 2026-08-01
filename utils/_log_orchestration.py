from typing import Any
import datetime
from dataclasses import asdict

_log_buffer: list[dict[str, Any]] = []

def _log_orchestration(gs: dict[str, Any], decision: Any) -> None:
    entry: dict[str, Any] = {
        "timestamp":  datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="milliseconds") + "Z",
        "agent":      "Orchestrator",
        "input_keys": sorted(gs.keys()),
        "output":     asdict(decision) if hasattr(decision, "__dataclass_fields__") else str(decision),
    }
    _log_buffer.append(entry)
