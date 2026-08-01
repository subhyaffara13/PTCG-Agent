
def test_apply_with_mutated_index():
    # GH 15169
    index = date_range("1-1-2015", "12-31-15", freq="D")
    df = DataFrame(
        data={"col1": np.random.default_rng(2).random(len(index))}, index=index
    )

    def f(x):
        s = Series([1, 2], index=["a", "b"])
        return s

    expected = df.groupby(pd.Grouper(freq="ME")).apply(f)

    result = df.resample("ME").apply(f)
    tm.assert_frame_equal(result, expected)

    # A case for series
    expected = df["col1"].groupby(pd.Grouper(freq="ME"), group_keys=False).apply(f)
    result = df["col1"].resample("ME").apply(f)
    tm.assert_series_equal(result, expected)

