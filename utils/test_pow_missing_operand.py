
def test_pow_missing_operand():
    # GH 55512
    k = pd.Series([2, None], dtype="int64[pyarrow]")
    result = k.pow(None, fill_value=3)
    expected = pd.Series([8, None], dtype="int64[pyarrow]")
    tm.assert_series_equal(result, expected)

