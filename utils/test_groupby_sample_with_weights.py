
def test_groupby_sample_with_weights(index, expected_index):
    # GH 39927 - tests for integer index needed
    values = [1] * 2 + [2] * 2
    df = DataFrame({"a": values, "b": values}, index=Index(index))

    result = df.groupby("a").sample(n=2, replace=True, weights=[1, 0, 1, 0])
    expected = DataFrame({"a": values, "b": values}, index=Index(expected_index))
    tm.assert_frame_equal(result, expected)

    result = df.groupby("a")["b"].sample(n=2, replace=True, weights=[1, 0, 1, 0])
    expected = Series(values, name="b", index=Index(expected_index))
    tm.assert_series_equal(result, expected)

