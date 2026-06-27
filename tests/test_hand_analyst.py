"""
tests/test_hand_analyst.py

Unit tests for agents/hand_analyst.py.
"""

import os
import json
import pytest
from pathlib import Path
from agents.hand_analyst import HandAnalyst
from router.bus import HandAnalystPacket

def test_hand_analyst_basic(tmp_path):
    skills_dir = tmp_path / "skills"
    skills_dir.mkdir()
    
    # Minimal card scoring database
    cards_file = skills_dir / "card_scoring.json"
    cards_file.write_text(json.dumps({
        "cards": [
            {"card_id": "1", "card_name": "Pikachu", "card_type": "Pokemon", "ev_score": 0.8, "combo_tags": ["Basic"]},
            {"card_id": "2", "card_name": "Supporter Draw", "card_type": "Trainer", "ev_score": 0.6, "combo_tags": ["Supporter"]},
            {"card_id": "3", "card_name": "Energy", "card_type": "Energy", "ev_score": 0.5, "combo_tags": []}
        ]
    }), encoding="utf-8")

    analyst = HandAnalyst(log_dir=str(tmp_path), skills_dir=str(skills_dir))
    
    # Pass valid packet type
    packet = HandAnalystPacket(hand=["pikachu", "supporter draw", "energy"], deck_remaining=30)
    
    res = analyst.receive(packet)
    
    assert res["hand_score"] > 0.0
    assert res["top_play"] == "pikachu"
    assert res["priority_profile"] in ("aggressive", "tempo", "defensive")
    
    # Assert logs/reasoning_log.json was written
    analyst.flush_logs()
    assert (tmp_path / "reasoning_log.json").exists()
