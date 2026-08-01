
def test_plan_prize_take_no_prized_ids():
    result = PrizeTracker().plan_prize_take(0, "", {}, 0)
    assert result["target"] == "active"
    assert result["reason"] == "unknown_prizes"

