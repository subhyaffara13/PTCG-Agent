
def test_fy5253_last_onoffset():
    # GH#18877 dates on the year-end but not normalized to midnight
    offset = FY5253(n=-5, startingMonth=5, variation="last", weekday=0)
    ts = Timestamp("1984-05-28 06:29:43.955911354+0200", tz="Europe/San_Marino")
    fast = offset.is_on_offset(ts)
    slow = (ts + offset) - offset == ts
    assert fast == slow

