
def test_datetime_tz_cut_mismatched_tzawareness(box):
    # GH#54964
    bins = box(
        [
            Timestamp("2013-01-01 04:57:07.200000"),
            Timestamp("2013-01-01 21:00:00"),
            Timestamp("2013-01-02 13:00:00"),
            Timestamp("2013-01-03 05:00:00"),
        ]
    )
    ser = Series(date_range("20130101", periods=3, tz="US/Eastern"))

    msg = "Cannot use timezone-naive bins with timezone-aware values"
    with pytest.raises(ValueError, match=msg):
        cut(ser, bins)

