
def test_to_datetime_with_empty_str_utc_false_format_mixed():
    # GH 50887
    vals = ["2020-01-01 00:00+00:00", ""]
    result = to_datetime(vals, format="mixed")
    expected = Index([Timestamp("2020-01-01 00:00+00:00"), "NaT"], dtype="M8[us, UTC]")
    tm.assert_index_equal(result, expected)

    # Check that a couple of other similar paths work the same way
    alt = to_datetime(vals)
    tm.assert_index_equal(alt, expected)
    alt2 = DatetimeIndex(vals)
    tm.assert_index_equal(alt2, expected)

