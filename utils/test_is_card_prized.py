
def test_is_card_prized():
    tracker = PrizeTracker(PRIZE_DECK_6)
    tracker.on_deck_search(["1"], ["2"], [], ["3", "3"], 2)
    assert tracker.is_card_prized(1) is True
    assert tracker.is_card_prized(2) is True
    assert tracker.is_card_prized(3) is False

