"""File I/O helpers for StrategyAgent — skill loading and strategy logging."""

from __future__ import annotations
import json
import pathlib
import datetime
from typing import Any

from cb_agents.log_flusher import flush_reasoning_logs
import logging

logger = logging.getLogger(__name__)

_PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
_SKILL_PATH   = _PROJECT_ROOT / "skills" / "strategy_profiles.json"
_LOG_PATH     = _PROJECT_ROOT / "logs"   / "reasoning_log.json"
_log_buffer: list[dict[str, Any]] = []


from utils.flush_logs import flush_logs


from utils.load_skill import load_skill


from utils.log_strategy import log_strategy


from utils.board_signal_match import board_signal_match


from utils.keyword_scan import keyword_scan
