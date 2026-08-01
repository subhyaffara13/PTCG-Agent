
def test_first_last_extension_array_keeps_dtype(values, function):
    # https://github.com/pandas-dev/pandas/issues/33071
    # https://github.com/pandas-dev/pandas/issues/32194
    df = DataFrame({"a": [1, 2], "b": values})
    grouped = df.groupby("a")
    idx = Index([1, 2], name="a")
    expected_series = Series(values, name="b", index=idx)
    expected_frame = DataFrame({"b": values}, index=idx)

    result_series = getattr(grouped["b"], function)()
    tm.assert_series_equal(result_series, expected_series)

    result_frame = grouped.agg({"b": function})
    tm.assert_frame_equal(result_frame, expected_frame)

