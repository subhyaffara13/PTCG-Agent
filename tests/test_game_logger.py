"""
tests/test_game_logger.py

Verifies the correctness and safety rules of factory/game_logger.py.
"""

import os
import json
import pytest
from pathlib import Path
from router.bus import RouterBus, StrategyPacket
from factory.game_logger import GameLogger


@pytest.fixture(autouse=True)
from utils.force_slow_sim import force_slow_sim


from utils.test_game_logger_creation_and_streams import test_game_logger_creation_and_streams


from utils.test_game_logger_logging_functions import test_game_logger_logging_functions


from utils.test_game_logger_save_creates_files import test_game_logger_save_creates_files


from utils.test_game_logger_auto_hook_router import test_game_logger_auto_hook_router
