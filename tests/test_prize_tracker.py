"""
tests/test_prize_tracker.py
Unit tests for cb_agents/prize_tracker.py.
"""
from cb_agents.prize_tracker import PrizeTracker
from test_prize_tracker_helpers import (
    DECK_PIKA_RAICHU, VISIBLE_PIKA_RAICHU, DECK_DICT,
    HAND, DISCARD, BOARD, DECK_CONTENTS, PRIZE_DECK_6, PRIZE_DECK_3
)

def test_prize_tracker_calculation():
    tracker = PrizeTracker(DECK_PIKA_RAICHU)
    probs = tracker.calculate_prized_probabilities(VISIBLE_PIKA_RAICHU, prizes_remaining=2)
    assert round(probs[721], 2) == 0.70
    assert round(probs[722], 2) == 0.40

def test_on_deck_search_deduction():
    tracker = PrizeTracker()
    tracker.record_initial_decklist(DECK_DICT)
    prized = tracker.on_deck_search(HAND, DISCARD, BOARD, DECK_CONTENTS, 48)
    assert tracker._deck_search_used is True
    assert prized.get(721) == 1
    assert prized.get(722) == 1
    assert prized.get(5) == 3
    assert prized.get(3) == 44
    enrichment = tracker.get_certainty_enrichment()
    assert enrichment["prize_certainty"] == 1.0
    assert enrichment["prizes_remaining"] == 49

def test_on_deck_search_before_initial_list():
    tracker = PrizeTracker()
    prized = tracker.on_deck_search(["1"], [], [], ["2"], 10)
    assert prized == {}
    assert tracker._deck_search_used is False

def test_get_certainty_enrichment_before_search():
    assert PrizeTracker().get_certainty_enrichment() == {}

def test_get_certainty_enrichment_after_search():
    tracker = PrizeTracker(PRIZE_DECK_6)
    tracker.on_deck_search(["1", "2"], [], ["3"], [], 3)
    enrichment = tracker.get_certainty_enrichment()
    assert enrichment["prize_certainty"] == 1.0
    assert enrichment["prizes_remaining"] == 3
    assert 1 in enrichment["prized_card_ids"]

def test_is_card_prized():
    tracker = PrizeTracker(PRIZE_DECK_6)
    tracker.on_deck_search(["1"], ["2"], [], ["3", "3"], 2)
    assert tracker.is_card_prized(1) is True
    assert tracker.is_card_prized(2) is True
    assert tracker.is_card_prized(3) is False

def test_prices_remaining_no_search():
    assert PrizeTracker(PRIZE_DECK_3).prizes_remaining() == 0

def test_plan_prize_take_no_prized_ids():
    result = PrizeTracker().plan_prize_take(0, "", {}, 0)
    assert result["target"] == "active"
    assert result["reason"] == "unknown_prizes"

def test_plan_prize_take_close_game():
    tracker = PrizeTracker(PRIZE_DECK_6)
    tracker.on_deck_search(["1", "2", "3", "3"], [], [], [], 2)
    assert tracker.prizes_remaining() <= 2
    result = tracker.plan_prize_take(120, "{L}", {}, 50)
    assert result["priority"] == "finisher"
