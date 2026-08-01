
def test_bunched_yearends():
    # GH#14774 cases with two fiscal year-ends in the same calendar-year
    fy = FY5253(n=1, weekday=5, startingMonth=12, variation="nearest")
    dt = Timestamp("2004-01-01")
    assert fy.rollback(dt) == Timestamp("2002-12-28")
    assert (-fy)._apply(dt) == Timestamp("2002-12-28")
    assert dt - fy == Timestamp("2002-12-28")

    assert fy.rollforward(dt) == Timestamp("2004-01-03")
    assert fy._apply(dt) == Timestamp("2004-01-03")
    assert fy + dt == Timestamp("2004-01-03")
    assert dt + fy == Timestamp("2004-01-03")

    # Same thing, but starting from a Timestamp in the previous year.
    dt = Timestamp("2003-12-31")
    assert fy.rollback(dt) == Timestamp("2002-12-28")
    assert (-fy)._apply(dt) == Timestamp("2002-12-28")
    assert dt - fy == Timestamp("2002-12-28")

