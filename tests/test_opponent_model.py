"""
tests/test_opponent_model.py

Unit tests for agents/opponent_model.py.
Run with: pytest tests/test_opponent_model.py -v
"""

import math
import pytest
from agents.opponent_model import OpponentModel, OpponentModelPacket


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_packet(**overrides) -> OpponentModelPacket:
    """Return a minimal valid OpponentModelPacket, with optional field overrides."""
    defaults = dict(
        turn=1,
        newly_played_cards=[],
        opponent_active_pokemon=None,
        opponent_bench_count=0,
        opponent_hand_size=5,
        opponent_prizes_remaining=6,
        opponent_discard=[],
        game_phase="early",
    )
    defaults.update(overrides)
    return OpponentModelPacket(**defaults)


# ---------------------------------------------------------------------------
# Initialisation
# ---------------------------------------------------------------------------

class TestInit:
    def test_perspective_flag(self):
        model = OpponentModel()
        assert model.perspective_flag == "opponent"

    def test_initial_priors_uniform(self):
        model = OpponentModel()
        confidences = list(model.inferred.archetype_confidence.values())
        if len(confidences) > 1:
            # All confidences should be roughly equal
            assert max(confidences) - min(confidences) < 1e-9

    def test_initial_priors_sum_to_one(self):
        model = OpponentModel()
        total = sum(model.inferred.archetype_confidence.values())
        assert abs(total - 1.0) < 1e-9

    def test_revealed_state_starts_empty(self):
        model = OpponentModel()
        assert model.revealed.played_cards == []
        assert model.revealed.discard_pile == []
        assert model.revealed.prizes_remaining == 6


# ---------------------------------------------------------------------------
# Packet type enforcement
# ---------------------------------------------------------------------------

class TestPacketEnforcement:
    def test_rejects_non_packet(self):
        model = OpponentModel()
        with pytest.raises(TypeError, match="OpponentModel received an illegal packet type"):
            model.receive({"turn": 1})  # plain dict — should be rejected

    def test_rejects_none(self):
        model = OpponentModel()
        with pytest.raises(TypeError):
            model.receive(None)

    def test_accepts_valid_packet(self):
        model = OpponentModel()
        result = model.receive(make_packet())
        assert isinstance(result, dict)


# ---------------------------------------------------------------------------
# Response structure
# ---------------------------------------------------------------------------

class TestResponseContract:
    def test_response_has_all_keys(self):
        model = OpponentModel()
        result = model.receive(make_packet())
        assert "predicted_next_action" in result
        assert "archetype_confidence" in result
        assert "inferred_deck_type" in result

    def test_confidence_is_float_in_range(self):
        model = OpponentModel()
        result = model.receive(make_packet())
        conf = result["archetype_confidence"]
        assert isinstance(conf, float)
        assert 0.0 <= conf <= 1.0

    def test_deck_type_is_string(self):
        model = OpponentModel()
        result = model.receive(make_packet())
        assert isinstance(result["inferred_deck_type"], str)

    def test_predicted_action_is_string(self):
        model = OpponentModel()
        result = model.receive(make_packet())
        assert isinstance(result["predicted_next_action"], str)


# ---------------------------------------------------------------------------
# RevealedState updates
# ---------------------------------------------------------------------------

class TestRevealedState:
    def test_newly_played_cards_accumulated(self):
        model = OpponentModel()
        model.receive(make_packet(newly_played_cards=["card_A"], turn=1))
        model.receive(make_packet(newly_played_cards=["card_B"], turn=2))
        assert "card_A" in model.revealed.played_cards
        assert "card_B" in model.revealed.played_cards

    def test_no_duplicate_played_cards(self):
        model = OpponentModel()
        model.receive(make_packet(newly_played_cards=["card_A"], turn=1))
        model.receive(make_packet(newly_played_cards=["card_A"], turn=2))
        assert model.revealed.played_cards.count("card_A") == 1

    def test_discard_pile_merged(self):
        model = OpponentModel()
        model.receive(make_packet(opponent_discard=["card_X"], turn=1))
        model.receive(make_packet(opponent_discard=["card_X", "card_Y"], turn=2))
        assert model.revealed.discard_pile.count("card_X") == 1
        assert "card_Y" in model.revealed.discard_pile

    def test_prizes_remaining_updated(self):
        model = OpponentModel()
        model.receive(make_packet(opponent_prizes_remaining=4, turn=1))
        assert model.revealed.prizes_remaining == 4

    def test_turn_count_updated(self):
        model = OpponentModel()
        model.receive(make_packet(turn=7))
        assert model.revealed.turn_count == 7

    def test_active_pokemon_updated(self):
        model = OpponentModel()
        model.receive(make_packet(opponent_active_pokemon="charizard-ex"))
        assert model.revealed.active_pokemon == "charizard-ex"


# ---------------------------------------------------------------------------
# Bayesian confidence update
# ---------------------------------------------------------------------------

class TestBayesianUpdate:
    def test_confidence_still_sums_to_one_after_update(self):
        model = OpponentModel()
        model.receive(make_packet(newly_played_cards=["some_card"]))
        total = sum(model.inferred.archetype_confidence.values())
        assert abs(total - 1.0) < 1e-9

    def test_repeated_updates_stay_bounded(self):
        model = OpponentModel()
        for i in range(20):
            model.receive(make_packet(newly_played_cards=[f"card_{i}"], turn=i + 1))
        for conf in model.inferred.archetype_confidence.values():
            assert 0.0 <= conf <= 1.0

    def test_confidence_rounded_to_4dp(self):
        model = OpponentModel()
        result = model.receive(make_packet())
        # confidence should be a clean 4dp float
        assert result["archetype_confidence"] == round(result["archetype_confidence"], 4)


# ---------------------------------------------------------------------------
# Prediction overrides
# ---------------------------------------------------------------------------

class TestPredictionOverrides:
    def test_low_hand_early_game_predicts_supporter(self):
        model = OpponentModel()
        # Inject a confident aggro prior to avoid unknown
        if "aggro" in model.inferred.archetype_priors:
            for k in model.inferred.archetype_priors:
                model.inferred.archetype_priors[k] = -10.0
            model.inferred.archetype_priors["aggro"] = 0.0
            model._normalise_priors()
        result = model.receive(make_packet(
            opponent_hand_size=2,
            game_phase="early",
        ))
        assert result["predicted_next_action"] == "play_supporter"


# ---------------------------------------------------------------------------
# Snapshot & reset
# ---------------------------------------------------------------------------

class TestSnapshotAndReset:
    def test_snapshot_has_both_states(self):
        model = OpponentModel()
        snap = model.snapshot()
        assert "revealed" in snap
        assert "inferred" in snap

    def test_reset_clears_game_state(self):
        model = OpponentModel()
        model.receive(make_packet(newly_played_cards=["card_A"], turn=3))
        model.reset()
        assert model.revealed.played_cards == []
        assert model.revealed.turn_count == 0

    def test_reset_reinitialises_priors(self):
        model = OpponentModel()
        model.receive(make_packet(newly_played_cards=["card_A"]))
        model.reset()
        total = sum(model.inferred.archetype_confidence.values())
        if model.inferred.archetype_confidence:
            assert abs(total - 1.0) < 1e-9
