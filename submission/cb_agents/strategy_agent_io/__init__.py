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

from .flush_logs_load_skill_log_strategy import flush_logs
from .flush_logs_load_skill_log_strategy import load_skill
from .flush_logs_load_skill_log_strategy import log_strategy
from .flush_logs_load_skill_log_strategy import _opponent_archetype_signal
from .board_signal_match_keyword_scan import board_signal_match
from .board_signal_match_keyword_scan import keyword_scan
