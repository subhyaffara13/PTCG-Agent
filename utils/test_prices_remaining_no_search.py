
def test_prices_remaining_no_search():
    assert PrizeTracker(PRIZE_DECK_3).prizes_remaining() == 0

