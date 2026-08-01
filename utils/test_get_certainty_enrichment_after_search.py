
def test_get_certainty_enrichment_after_search():
    tracker = PrizeTracker(PRIZE_DECK_6)
    tracker.on_deck_search(["1", "2"], [], ["3"], [], 3)
    enrichment = tracker.get_certainty_enrichment()
    assert enrichment["prize_certainty"] == 1.0
    assert enrichment["prizes_remaining"] == 3
    assert 1 in enrichment["prized_card_ids"]

