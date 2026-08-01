
def test_fy5253_nearest_onoffset():
    # GH#18877 dates on the year-end but not normalized to midnight
    offset = FY5253(n=3, startingMonth=7, variation="nearest", weekday=2)
    ts = Timestamp("2032-07-28 00:12:59.035729419+0000", tz="Africa/Dakar")
    fast = offset.is_on_offset(ts)
    slow = (ts + offset) - offset == ts
    assert fast == slow

