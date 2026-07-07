"""
tests/test_strategy_agent.py

Unit tests for cb_agents/strategy_agent.py.
"""

import os
import json
import pytest
from pathlib import Path
from cb_agents.strategy_agent import StrategyAgent
from router.bus import StrategyPacket

def test_strategy_agent_triggers(tmp_path):
    skills_dir = tmp_path / "skills"
    skills_dir.mkdir()
    
    # Save a minimal strategy file
    strategy_file = skills_dir / "strategy_profiles.json"
    strategy_file.write_text(json.dumps({"profiles": {"setup": {"actions": ["PASS"]}, "hand_dead": {"actions": ["PASS"]}, "aggro_push": {"actions": ["PASS"]}}}), encoding="utf-8")

    agent = StrategyAgent(log_dir=str(tmp_path), skills_dir=str(skills_dir))
    
    # 1. No trigger condition met
    state_normal = {
        "my_prizes_remaining": 6,
        "opponent_prizes_remaining": 6,
        "opponent_archetype_confidence": 0.1,
        "priority_profile": "aggro_push",
        "turn_number": 1
    }
    
    p1 = StrategyPacket(trigger="turn_start", board_summary=state_normal)
    r1 = agent.receive(p1)
    
    assert "strategy" in r1
    
    # 2. Trigger check: explicit force_evaluate
    p2 = StrategyPacket(trigger="force_evaluate", board_summary=state_normal)
    r2 = agent.receive(p2)
    assert "strategy" in r2

    # 3. Trigger check: prize gap threshold >= 2
    state_gap = {
        "my_prizes_remaining": 5,
        "opponent_prizes_remaining": 3,
        "opponent_archetype_confidence": 0.1,
        "priority_profile": "aggro_push",
        "turn_number": 2
    }
    p3 = StrategyPacket(trigger="prize_gap_check", board_summary=state_gap)
    r3 = agent.receive(p3)
    assert "strategy" in r3
