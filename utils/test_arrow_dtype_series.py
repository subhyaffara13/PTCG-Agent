
def test_arrow_dtype_series(dtype, exp_dtype):
    pytest.importorskip("pyarrow")

    cols = ["a", "b"]
    series_a = Series([1, 2], index=cols, dtype="int32")
    df_b = DataFrame([[1, 0], [0, 1]], index=cols, dtype=dtype)
    result = series_a.dot(df_b)
    expected = Series([1, 2], dtype=exp_dtype)

    tm.assert_series_equal(result, expected)

