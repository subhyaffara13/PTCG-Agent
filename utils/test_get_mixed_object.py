
def test_get_mixed_object():
    ser = Series(["a_b_c", np.nan, "c_d_e", True, datetime.today(), None, 1, 2.0])
    result = ser.str.split("_").str.get(1)
    expected = Series(
        ["b", np.nan, "d", np.nan, np.nan, None, np.nan, np.nan], dtype=object
    )
    tm.assert_series_equal(result, expected)

