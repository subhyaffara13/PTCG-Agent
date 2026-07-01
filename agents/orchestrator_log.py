"""Logging helper for Orchestrator decisions."""

from __future__ import annotations
import json
import pathlib
import datetime
from dataclasses import asdict
from typing import Any
from agents.log_flusher import flush_reasoning_logs
import logging

logger = logging.getLogger(__name__)

_PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
_LOG_PATH     = _PROJECT_ROOT / "logs" / "reasoning_log.json"
_log_buffer: list[dict[str, Any]] = []


def flush_logs() -> None:
    _LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    flush_reasoning_logs(_log_buffer, _LOG_PATH, logger)


def _log_orchestration(gs: dict[str, Any], decision: Any) -> None:
    entry: dict[str, Any] = {
        "timestamp":  datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="milliseconds") + "Z",
        "agent":      "Orchestrator",
        "input_keys": sorted(gs.keys()),
        "output":     asdict(decision),
    }
    _log_buffer.append(entry)
