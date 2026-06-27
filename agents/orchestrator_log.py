"""Logging helper for Orchestrator decisions."""

from __future__ import annotations
import json
import pathlib
import datetime
from dataclasses import asdict
from typing import Any

_PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
_LOG_PATH     = _PROJECT_ROOT / "logs" / "reasoning_log.json"
_log_buffer: list[dict[str, Any]] = []


def flush_logs() -> None:
    if not _log_buffer:
        return
    _LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    try:
        log: list[Any] = json.loads(_LOG_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, FileNotFoundError):
        log = []
    log.extend(_log_buffer)
    _LOG_PATH.write_text(json.dumps(log, indent=2), encoding="utf-8")
    _log_buffer.clear()


def _log_orchestration(gs: dict[str, Any], decision: Any) -> None:
    entry: dict[str, Any] = {
        "timestamp":  datetime.datetime.utcnow().isoformat(timespec="milliseconds") + "Z",
        "agent":      "Orchestrator",
        "input_keys": sorted(gs.keys()),
        "output":     asdict(decision),
    }
    _log_buffer.append(entry)
