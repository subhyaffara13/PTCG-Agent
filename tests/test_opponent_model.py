"""
tests/test_opponent_model.py

Unit tests for cb_agents/opponent_model.py.
"""

import pytest
from cb_agents.opponent_model import OpponentModel
from router.bus import OpponentModelPacket


from utils.make_packet import make_packet


class TestOpponentModel:
    def test_init(self):
        model = OpponentModel()
        assert model.perspective_flag == "opponent"
        assert len(model.revealed_state) == 0
        assert model.archetype_confidence == 0.0

    def test_type_enforcement(self):
        model = OpponentModel()
        with pytest.raises(TypeError):
            model.receive("not a packet")

    def test_confidence_limit_under_3_cards(self):
        # Confidence remains 0.0 until at least 3 cards are revealed (for non-signature pool cards)
        model = OpponentModel()
        
        # Mock some archetypes data
        model.archetypes = {
            "aggro": {"signature_cards": ["1", "2", "3"], "card_pool": ["10", "20", "30"]}
        }
        
        packet = make_packet(newly_played_cards=["10", "20"])
        res = model.receive(packet)
        assert res["archetype_confidence"] == 0.0

    def test_predict_aggro(self):
        model = OpponentModel()
        model.archetypes = {
            "aggro": {"signature_cards": ["1", "2", "3"], "card_pool": []}
        }
        
        packet = make_packet(newly_played_cards=["1", "2", "3"], revealed_prizes_remaining=5)
        res = model.receive(packet)
        assert res["inferred_deck_type"] == "aggro"
        assert res["predicted_next_action"] == "attack"
