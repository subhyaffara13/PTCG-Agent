
def test_arrow_true_division_large_divisor(dtype):
    # GH 56706
    a = pd.Series([0], dtype=dtype)
    b = pd.Series([18014398509481983], dtype=dtype)
    expected = pd.Series([0], dtype="float64[pyarrow]")
    result = a / b
    tm.assert_series_equal(result, expected)

