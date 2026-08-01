
def test_plan_prize_take_close_game():
    tracker = PrizeTracker(PRIZE_DECK_6)
    tracker.on_deck_search(["1", "2", "3", "3"], [], [], [], 2)
    assert tracker.prizes_remaining() <= 2
    result = tracker.plan_prize_take(120, "{L}", {}, 50)
    assert result["priority"] == "finisher"

