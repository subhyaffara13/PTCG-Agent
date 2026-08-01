"""Logging helper for Orchestrator decisions."""

from __future__ import annotations
import json
import pathlib
import datetime
from dataclasses import asdict
from typing import Any
from cb_agents.log_flusher import flush_reasoning_logs
import logging

logger = logging.getLogger(__name__)

_PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
_LOG_PATH     = _PROJECT_ROOT / "logs" / "reasoning_log.json"
_log_buffer: list[dict[str, Any]] = []


from utils.flush_logs import flush_logs


from utils._log_orchestration import _log_orchestration
