
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

