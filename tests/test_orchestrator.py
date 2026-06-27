"""
tests/test_orchestrator.py

Unit tests for agents/orchestrator.py.
"""

import json
import time
import pytest
from pathlib import Path
from agents.orchestrator import Orchestrator

def test_orchestrator_initialization_and_turn(tmp_path):
    skills_dir = tmp_path / "skills"
    skills_dir.mkdir()
    
    # Write config mock files
    (skills_dir / "delegation_map.json").write_text(json.dumps({
        "delegation": {
            "turn_start": "hand_analyst",
            "after_hand_analysis": "turn_planner",
            "on_trigger": "strategy_agent",
            "on_opponent_play": "opponent_model",
            "before_turn_planner": "lethal_calculator",
            "always": "time_manager"
        }
    }), encoding="utf-8")
    
    (skills_dir / "card_scoring.json").write_text(json.dumps({"cards": []}), encoding="utf-8")
    (skills_dir / "priority_rules.json").write_text(json.dumps({"rules": []}), encoding="utf-8")
    (skills_dir / "strategy_profiles.json").write_text(json.dumps({"profiles": {"setup": {"actions": ["PASS"]}, "hand_dead": {"actions": ["PASS"]}}}), encoding="utf-8")
    (skills_dir / "deck_archetypes.json").write_text(json.dumps({"archetypes": {}}), encoding="utf-8")

    orchestrator = Orchestrator(log_dir=str(tmp_path), skills_dir=str(skills_dir))
    
    orchestrator.start_game()
    
    state = {
        "my_hand": ["1", "2"],
        "my_deck_count": 45,
        "my_prizes": 6,
        "opponent_prizes": 6,
        "my_active_hp": 100,
        "opponent_active_hp": 100,
        "opponent_last_play": False,
        "legal_attacks": ["Thunderbolt"]
    }
    
    action = orchestrator.run_turn(state)
    
    assert type(action).__name__ == "TurnDecision"
