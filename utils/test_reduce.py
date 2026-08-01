
def test_reduce():
    assert reduce(add)((1, 2, 3)) == 6


def test_reduce(string_series):
    # reductions with named functions
    result = string_series.agg(["sum", "mean"])
    expected = Series(
        [string_series.sum(), string_series.mean()],
        ["sum", "mean"],
        name=string_series.name,
    )
    tm.assert_series_equal(result, expected)


def test_reduce():
    df = DataFrame({"a": [1, 2, 3], "b": 1.5})

    result = df.sum()
    assert result.index is not df.columns

    result = df.groupby([0, 0, 1]).sum()
    assert result.columns is not df.columns

    result = df.quantile(0.5)
    assert result.index is not df.columns
    result = df.quantile([0.25, 0.5, 0.75])
    assert result.columns is not df.columns


def test_reduce(skipna, dtype):
    arr = pd.Series(["a", "b", "c"], dtype=dtype)
    result = arr.sum(skipna=skipna)
    assert result == "abc"

