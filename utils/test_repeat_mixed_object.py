
def test_repeat_mixed_object():
    ser = Series(["a", np.nan, "b", True, datetime.today(), "foo", None, 1, 2.0])
    result = ser.str.repeat(3)
    expected = Series(
        ["aaa", np.nan, "bbb", np.nan, np.nan, "foofoofoo", None, np.nan, np.nan],
        dtype=object,
    )
    tm.assert_series_equal(result, expected)

