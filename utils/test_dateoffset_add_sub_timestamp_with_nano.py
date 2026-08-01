
def test_dateoffset_add_sub_timestamp_with_nano():
    offset = DateOffset(minutes=2, nanoseconds=9)
    ts = Timestamp(4)
    result = ts + offset
    expected = Timestamp("1970-01-01 00:02:00.000000013")
    assert result == expected
    result -= offset
    assert result == ts
    result = offset + ts
    assert result == expected

    offset2 = DateOffset(minutes=2, nanoseconds=9, hour=1)
    assert offset2._use_relativedelta
    with tm.assert_produces_warning(None):
        # no warning about Discarding nonzero nanoseconds
        result2 = ts + offset2
    expected2 = Timestamp("1970-01-01 01:02:00.000000013")
    assert result2 == expected2

