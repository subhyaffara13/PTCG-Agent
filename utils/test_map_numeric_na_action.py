
def test_map_numeric_na_action(using_nan_is_na):
    ser = pd.Series([32, 40, None], dtype="int64[pyarrow]")
    result = ser.map(lambda x: 42, na_action="ignore")
    if not using_nan_is_na:
        expected = pd.Series([42.0, 42.0, pd.NA], dtype="object")
    else:
        expected = pd.Series([42.0, 42.0, np.nan], dtype="float64")
    tm.assert_series_equal(result, expected)

