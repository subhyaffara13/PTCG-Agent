
def test_on_deck_search_before_initial_list():
    tracker = PrizeTracker()
    prized = tracker.on_deck_search(["1"], [], [], ["2"], 10)
    assert prized == {}
    assert tracker._deck_search_used is False

