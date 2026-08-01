
def test_arrow_floordiv_large_integral_result(dtype):
    # GH 56676
    a = pd.Series([18014398509481983], dtype=dtype)
    result = a // 1
    tm.assert_series_equal(result, a)

