
def test_pow_with_all_na_float():
    # GH#62520

    s = pd.Series([None, None], dtype="float64[pyarrow]")
    result = s.pow(2)
    expected = pd.Series([pd.NA, pd.NA], dtype="float64[pyarrow]")
    tm.assert_series_equal(result, expected)

