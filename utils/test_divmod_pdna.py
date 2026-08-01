
def test_divmod_pdna(dtype):
    # GH#62196
    ser = pd.Series([1, 2, 3], dtype=dtype)
    res = divmod(pd.NA, ser)
    assert isinstance(res, tuple) and len(res) == 2

    exp = pd.Series([pd.NA, pd.NA, pd.NA], dtype=dtype)
    tm.assert_series_equal(res[0], exp)
    tm.assert_series_equal(res[1], exp)

    tm.assert_series_equal(res[0], pd.NA // ser)
    tm.assert_series_equal(res[1], pd.NA % ser)

    res = divmod(ser, pd.NA)
    assert isinstance(res, tuple) and len(res) == 2
    tm.assert_series_equal(res[0], exp)
    tm.assert_series_equal(res[1], exp)

    tm.assert_series_equal(res[0], ser // pd.NA)
    tm.assert_series_equal(res[1], ser % pd.NA)

