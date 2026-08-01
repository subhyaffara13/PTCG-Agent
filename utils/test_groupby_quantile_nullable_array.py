
def test_groupby_quantile_nullable_array(values, q):
    # https://github.com/pandas-dev/pandas/issues/33136
    df = DataFrame({"a": ["x"] * 3 + ["y"] * 3, "b": values})
    result = df.groupby("a")["b"].quantile(q)

    if isinstance(q, list):
        idx = pd.MultiIndex.from_product((["x", "y"], q), names=["a", None])
        true_quantiles = [0.0, 0.5, 1.0]
    else:
        idx = Index(["x", "y"], name="a")
        true_quantiles = [0.5]

    expected = pd.Series(true_quantiles * 2, index=idx, name="b", dtype="Float64")
    tm.assert_series_equal(result, expected)

