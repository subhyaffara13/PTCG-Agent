"""
tests/test_game_runner.py

Unit tests for factory/game_runner.py.
"""

import os
import json
import pytest
from pathlib import Path
from factory.game_runner import GameRunner

def test_game_runner_three_games(tmp_path):
    runner = GameRunner(log_dir=str(tmp_path))
    
    deck_base = {"pokemon": ["Pikachu"]}
    deck_new = {"pokemon": ["Charizard"]}
    reasoning_base = {"strategy": "aggro"}
    reasoning_new = {"strategy": "control"}
    
    res = runner.run_iteration(
        iteration_id=1,
        version_n1="1.0.0",
        version_n2="1.1.0",
        deck_base=deck_base,
        deck_new=deck_new,
        reasoning_base=reasoning_base,
        reasoning_new=reasoning_new
    )
    
    assert res["iteration"] == 1
    assert res["ready_for_eval"] is True
    assert "reasoning_test" in res["games"]
    assert "deck_test" in res["games"]
    assert "variance_baseline" in res["games"]
    
    # Assert iteration result file was saved
    res_file = tmp_path / "iteration_result.json"
    assert res_file.exists()
    
    saved_data = json.loads(res_file.read_text(encoding="utf-8"))
    assert saved_data["ready_for_eval"] is True
