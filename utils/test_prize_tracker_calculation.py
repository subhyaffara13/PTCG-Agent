
def test_prize_tracker_calculation():
    tracker = PrizeTracker(DECK_PIKA_RAICHU)
    probs = tracker.calculate_prized_probabilities(VISIBLE_PIKA_RAICHU, prizes_remaining=2)
    assert round(probs[721], 2) == 0.70
    assert round(probs[722], 2) == 0.40

