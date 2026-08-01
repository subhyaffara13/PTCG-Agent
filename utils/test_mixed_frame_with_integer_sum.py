
def test_mixed_frame_with_integer_sum():
    # https://github.com/pandas-dev/pandas/issues/34520
    df = DataFrame([["a", 1]], columns=list("ab"))
    df = df.astype({"b": "Int64"})
    result = df.sum()
    expected = Series(["a", 1], index=["a", "b"])
    tm.assert_series_equal(result, expected)

