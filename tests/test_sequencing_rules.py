"""
tests/test_sequencing_rules.py

Unit tests for new sequencing heuristics and prize-aware strategy switching.
"""
import json
import pytest
from agents.turn_planner import TurnPlanner
from agents.strategy_agent import StrategyAgent
from router.bus import TurnPlannerPacket, StrategyPacket
from test_sequencing_rules_helpers import (
    setup_skills_dir, PRIORITY_RULES_EMPTY, STRATEGY_PROFILES_EMPTY, CHARGED_ACTIVE
)

def test_supporter_first_priority(tmp_path):
    setup_skills_dir(tmp_path, "priority_rules.json", PRIORITY_RULES_EMPTY)
    planner = TurnPlanner(log_dir=str(tmp_path), skills_dir=str(tmp_path / "skills"))
    packet = TurnPlannerPacket(hand_score=0.5, priority_profile="aggro_push", top_play="none", game_state={
        "legal_trainers": ["Ultra Ball", "Professor's Research", "Pok\u00e9 Ball"],
        "my_active_pokemon": None, "my_hand": [1, 2, 3, 4]
    }, turn=1)
    trainers = [a for a in planner.receive(packet)["action_sequence"] if a.startswith("play_trainer:")]
    assert trainers[0] == "play_trainer:Professor's Research"

def test_energy_over_attachment_prevention(tmp_path):
    setup_skills_dir(tmp_path, "priority_rules.json", PRIORITY_RULES_EMPTY)
    planner = TurnPlanner(log_dir=str(tmp_path), skills_dir=str(tmp_path / "skills"))
    packet = TurnPlannerPacket(hand_score=0.8, priority_profile="aggro_push", top_play="none", game_state={
        "legal_attachments": ["Active"], "legal_attacks": ["Thunderbolt"],
        "my_active_pokemon": CHARGED_ACTIVE
    }, turn=1)
    seq = planner.receive(packet)["action_sequence"]
    assert seq.index("attach_energy:Active") > seq.index("attack:Thunderbolt")

def test_prized_attacker_strategy_switch(tmp_path):
    setup_skills_dir(tmp_path, "strategy_profiles.json", STRATEGY_PROFILES_EMPTY)
    agent = StrategyAgent(log_dir=str(tmp_path), skills_dir=str(tmp_path / "skills"))
    res = agent.receive(StrategyPacket(trigger="turn_start", board_summary={
        "my_prizes_remaining": 6, "opponent_prizes_remaining": 6,
        "opponent_confidence": 0.1, "priority_profile": "aggro_push",
        "turn_number": 2, "prized_probabilities": {"721": 0.85}
    }))
    assert res["strategy"] == "early_game_setup"
