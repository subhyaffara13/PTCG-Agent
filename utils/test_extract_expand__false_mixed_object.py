
def test_extract_expand_False_mixed_object():
    ser = Series(
        ["aBAD_BAD", np.nan, "BAD_b_BAD", True, datetime.today(), "foo", None, 1, 2.0]
    )

    # two groups
    result = ser.str.extract(".*(BAD[_]+).*(BAD)", expand=False)
    er = [np.nan, np.nan]  # empty row
    expected = DataFrame(
        [["BAD_", "BAD"], er, ["BAD_", "BAD"], er, er, er, er, er, er], dtype=object
    )
    tm.assert_frame_equal(result, expected)

    # single group
    result = ser.str.extract(".*(BAD[_]+).*BAD", expand=False)
    expected = Series(
        ["BAD_", np.nan, "BAD_", np.nan, np.nan, np.nan, None, np.nan, np.nan],
        dtype=object,
    )
    tm.assert_series_equal(result, expected)

