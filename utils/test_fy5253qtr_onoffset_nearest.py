
def test_fy5253qtr_onoffset_nearest():
    # GH#19036
    ts = Timestamp("1985-09-02 23:57:46.232550356-0300", tz="Atlantic/Bermuda")
    offset = FY5253Quarter(
        n=3, qtr_with_extra_week=1, startingMonth=2, variation="nearest", weekday=0
    )
    fast = offset.is_on_offset(ts)
    slow = (ts + offset) - offset == ts
    assert fast == slow

