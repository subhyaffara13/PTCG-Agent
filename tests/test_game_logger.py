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


def test_game_logger_creation_and_streams(tmp_path):
    logger = GameLogger(log_dir=str(tmp_path))
    assert logger.perspective_flag == "player"
    assert len(logger.action_logs) == 0
    assert len(logger.reasoning_logs) == 0
    assert len(logger.variance_logs) == 0


def test_game_logger_logging_functions(tmp_path):
    gl = GameLogger(log_dir=str(tmp_path))
    gl.log_action(1, "strategy_agent", "on_trigger", {"cards": []}, {"cards": ["A"]})
    gl.log_reasoning(1, "aggro", 8.5, False, 0.45, "Chain text", True, "positive")
    gl.log_variance(1, "coin_flip", "heads", "tails", -1.0)
    
    assert len(gl.action_logs) == 1
    assert len(gl.reasoning_logs) == 1
    assert len(gl.variance_logs) == 1
    
    assert gl.action_logs[0]["turn"] == 1
    assert gl.reasoning_logs[0]["reasoning_outcome"] == "positive"
    assert gl.variance_logs[0]["event_type"] == "coin_flip"


def test_game_logger_save_creates_files(tmp_path):
    gl = GameLogger(log_dir=str(tmp_path))
    gl.log_action(1, "strategy_agent", "on_trigger", {"cards": []}, {"cards": ["A"]})
    gl.log_reasoning(1, "aggro", 8.5, False, 0.45, "Chain text", True, "positive")
    gl.log_variance(1, "coin_flip", "heads", "tails", -1.0)
    
    gl.save("base_v1", "new_v2")
    
    # Assert files are created
    files = list(tmp_path.glob("*.json"))
    assert len(files) == 3
    
    # Check naming conventions
    prefixes = {f.name.split("_")[0] for f in files}
    assert prefixes == {"action", "reasoning", "variance"}
    
    for f in files:
        assert "base_v1_vs_vnew_v2" in f.name


def test_game_logger_auto_hook_router(tmp_path):
    delegation = {"on_trigger": "strategy_agent"}
    bus = RouterBus(delegation, log_dir=str(tmp_path))
    bus.register_agent("strategy_agent", lambda p: {"result": "success"})
    
    gl = GameLogger(log_dir=str(tmp_path))
    gl.register_with_bus(bus)
    
    packet = StrategyPacket(trigger="turn_draw", board_summary={})
    res = bus.dispatch("on_trigger", packet)
    
    assert res == {"result": "success"}
    assert len(gl.action_logs) == 1
    assert gl.action_logs[0]["action_taken"] == "on_trigger"
    assert gl.action_logs[0]["agent_called"] == "strategy_agent"
