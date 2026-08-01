
def test_isin_large_series_mixed_dtypes_and_nan(monkeypatch):
    # https://github.com/pandas-dev/pandas/issues/37094
    # combination of object dtype for the values
    # and > _MINIMUM_COMP_ARR_LEN elements
    min_isin_comp = 5
    ser = Series([1, 2, np.nan] * min_isin_comp)
    with monkeypatch.context() as m:
        m.setattr(algorithms, "_MINIMUM_COMP_ARR_LEN", min_isin_comp)
        result = ser.isin({"foo", "bar"})
    expected = Series([False] * 3 * min_isin_comp)
    tm.assert_series_equal(result, expected)

