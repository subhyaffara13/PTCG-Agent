"""
tests/test_turn_planner.py

Unit tests for cb_agents/turn_planner.py.
"""

import os
import json
import pytest
from pathlib import Path
from cb_agents.turn_planner import TurnPlanner
from router.bus import TurnPlannerPacket

def test_turn_planner_sorting(tmp_path):
    skills_dir = tmp_path / "skills"
    skills_dir.mkdir()
    
    # Save a minimal rules file
    rules_file = skills_dir / "priority_rules.json"
    rules_file.write_text(json.dumps({"rules": []}), encoding="utf-8")

    planner = TurnPlanner(log_dir=str(tmp_path), skills_dir=str(skills_dir))
    
    # Setup test packet
    state = {
        "legal_attacks": ["Thunderbolt"],
        "legal_bench": ["Pikachu"],
        "legal_trainers": ["Professor Oak"]
    }
    
    packet = TurnPlannerPacket(
        hand_score=0.8,
        priority_profile="setup",
        top_play="Pikachu",
        game_state=state
    )
    
    res = planner.receive(packet)
    
    # Setup profile sorts bench first; no bench in state → bench:Pikachu is primary
    assert res["primary_action"] == "bench:Pikachu"
    assert "pass" in res["action_sequence"]
    
    # Verify fallback profile
    packet_bad_profile = TurnPlannerPacket(
        hand_score=0.8,
        priority_profile="invalid_profile_name",
        top_play="Pikachu",
        game_state=state
    )
    res_bad = planner.receive(packet_bad_profile)
    assert res_bad["primary_action"] == "bench:Pikachu"
