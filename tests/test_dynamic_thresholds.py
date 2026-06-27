"""
tests/test_dynamic_thresholds.py

Dynamic threshold and behavior alteration tests.
"""
import json
import pytest
from agents.hand_analyst import HandAnalyst
from agents.strategy_agent import StrategyAgent
from router.bus import HandAnalystPacket, StrategyPacket
from agents.context import SharedContext
from test_dynamic_thresholds_helpers import (
    make_card_scoring, INITIAL_THRESHOLDS, MODIFIED_THRESHOLDS
)

def test_dynamic_threshold_loading(tmp_path):
    skills_dir = tmp_path / "skills"
    skills_dir.mkdir()
    make_card_scoring(skills_dir)

    thresholds_file = skills_dir / "strategy_thresholds.json"
    thresholds_file.write_text(json.dumps(INITIAL_THRESHOLDS), encoding="utf-8")
    SharedContext._caches.clear()

    analyst = HandAnalyst(log_dir=str(tmp_path), skills_dir=str(skills_dir))
    agent = StrategyAgent(log_dir=str(tmp_path), skills_dir=str(skills_dir))

    packet_ha = HandAnalystPacket(hand=["1", "2", "3"], deck_remaining=30)
    analyst.receive(packet_ha)

    packet_sa = StrategyPacket(trigger="turn_start", board_summary={
        "my_prizes_remaining": 5,
        "opponent_prizes_remaining": 3,
        "opponent_archetype_confidence": 0.1,
        "priority_profile": "aggro_push",
        "turn_number": 2
    })
    res_sa_1 = agent.receive(packet_sa)
    assert res_sa_1["triggered"] is True

    thresholds_file.write_text(json.dumps(MODIFIED_THRESHOLDS), encoding="utf-8")

    res_sa_2 = agent.receive(packet_sa)
    print("Existing StrategyAgent triggered after modification:", res_sa_2["triggered"])
    print("Existing HandAnalyst score after modification:", analyst.receive(packet_ha)["hand_score"])

    new_agent = StrategyAgent(log_dir=str(tmp_path), skills_dir=str(skills_dir))
    res_sa_3 = new_agent.receive(packet_sa)
    print("New StrategyAgent triggered after modification:", res_sa_3["triggered"])

    SharedContext._caches.clear()
    fresh_agent = StrategyAgent(log_dir=str(tmp_path), skills_dir=str(skills_dir))
    res_sa_4 = fresh_agent.receive(packet_sa)
    print("Fresh StrategyAgent (cache cleared) triggered:", res_sa_4["triggered"])

    assert res_sa_2["triggered"] is True
    assert res_sa_3["triggered"] is True
    assert res_sa_4["triggered"] is False
