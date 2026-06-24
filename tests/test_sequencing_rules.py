"""
tests/test_sequencing_rules.py

Unit tests for new sequencing heuristics and prize-aware strategy switching.
"""

import json
import pytest
from pathlib import Path
from agents.turn_planner import TurnPlanner
from agents.strategy_agent import StrategyAgent
from router.bus import TurnPlannerPacket, StrategyPacket

def test_supporter_first_priority(tmp_path):
    skills_dir = tmp_path / "skills"
    skills_dir.mkdir()
    (skills_dir / "priority_rules.json").write_text(json.dumps({"rules": []}), encoding="utf-8")

    planner = TurnPlanner(log_dir=str(tmp_path), skills_dir=str(skills_dir))

    state = {
        "legal_trainers": ["Nest Ball", "Professor's Research", "Poké Ball"],
        "my_active_pokemon": None
    }

    packet = TurnPlannerPacket(
        hand_score=0.5,
        priority_profile="aggro_push",
        top_play="none",
        game_state=state,
        turn=1
    )

    res = planner.receive(packet)
    action_seq = res["action_sequence"]
    
    # Extract only play_trainer moves
    trainers = [a for a in action_seq if a.startswith("play_trainer:")]
    
    assert trainers[0] == "play_trainer:Nest Ball"
    assert "play_trainer:Professor's Research" in trainers
    assert "play_trainer:Poké Ball" in trainers

def test_energy_over_attachment_prevention(tmp_path):
    skills_dir = tmp_path / "skills"
    skills_dir.mkdir()
    (skills_dir / "priority_rules.json").write_text(json.dumps({"rules": []}), encoding="utf-8")

    planner = TurnPlanner(log_dir=str(tmp_path), skills_dir=str(skills_dir))

    # Active pokemon has ID 722 (needed = 3) and 3 energies attached
    active_charged = {
        "id": 722,
        "energies": [3, 3, 3]
    }

    state = {
        "legal_attachments": ["Active"],
        "legal_attacks": ["Thunderbolt"],
        "my_active_pokemon": active_charged
    }

    packet = TurnPlannerPacket(
        hand_score=0.8,
        priority_profile="aggro_push",
        top_play="none",
        game_state=state,
        turn=1
    )

    res = planner.receive(packet)
    action_seq = res["action_sequence"]
    
    # Since active is charged, attach_energy should be deprioritized below attacks
    energy_idx = action_seq.index("attach_energy:Active")
    attack_idx = action_seq.index("attack:Thunderbolt")
    
    assert energy_idx > attack_idx

def test_prized_attacker_strategy_switch(tmp_path):
    skills_dir = tmp_path / "skills"
    skills_dir.mkdir()
    (skills_dir / "strategy_profiles.json").write_text(json.dumps({"profiles": {}}), encoding="utf-8")

    agent = StrategyAgent(log_dir=str(tmp_path), skills_dir=str(skills_dir))

    # Prized probability for Pikachu (721) is 0.85
    board_state = {
        "my_prizes_remaining": 6,
        "opponent_prizes_remaining": 6,
        "opponent_confidence": 0.1,
        "priority_profile": "aggro_push",
        "turn_number": 2,
        "prized_probabilities": {
            "721": 0.85
        }
    }

    packet = StrategyPacket(
        trigger="turn_start",
        board_summary=board_state
    )

    res = agent.receive(packet)
    assert res["triggered"] is True
    assert res["new_strategy"] == "setup"
