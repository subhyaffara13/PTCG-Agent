
def test_apply_mixed_dtype_corner():
    df = DataFrame({"A": ["foo"], "B": [1.0]})
    result = df[:0].apply(np.mean, axis=1)
    # the result here is actually kind of ambiguous, should it be a Series
    # or a DataFrame?
    expected = Series(dtype=np.float64)
    tm.assert_series_equal(result, expected)

