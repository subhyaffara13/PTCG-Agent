
def test_len_mixed():
    ser = Series(
        ["a_b", np.nan, "asdf_cas_asdf", True, datetime.today(), "foo", None, 1, 2.0]
    )
    result = ser.str.len()
    expected = Series([3, np.nan, 13, np.nan, np.nan, 3, np.nan, np.nan, np.nan])
    tm.assert_series_equal(result, expected)

