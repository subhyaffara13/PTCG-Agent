
def test_str_replace_negative_n():
    # GH 56404
    ser = pd.Series(["abc", "aaaaaa"], dtype=ArrowDtype(pa.string()))
    actual = ser.str.replace("a", "", -3, True)
    expected = pd.Series(["bc", ""], dtype=ArrowDtype(pa.string()))
    tm.assert_series_equal(expected, actual)

    # Same bug for pyarrow-backed StringArray GH#59628
    ser2 = ser.astype(pd.StringDtype(storage="pyarrow"))
    actual2 = ser2.str.replace("a", "", -3, True)
    expected2 = expected.astype(ser2.dtype)
    tm.assert_series_equal(expected2, actual2)

    ser3 = ser.astype(pd.StringDtype(storage="pyarrow", na_value=np.nan))
    actual3 = ser3.str.replace("a", "", -3, True)
    expected3 = expected.astype(ser3.dtype)
    tm.assert_series_equal(expected3, actual3)

