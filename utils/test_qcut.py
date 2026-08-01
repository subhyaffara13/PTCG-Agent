
def test_qcut() -> None:
    # https://github.com/pandas-dev/pandas/pull/63439
    df = pd.DataFrame({"a": [1, 2, 3]})
    expr = pd.qcut(pd.col("a"), 3)
    expected_str = "qcut(x=col('a'), q=3, labels=None, retbins=False, precision=3)"
    assert str(expr) == expected_str, str(expr)

    result = df.assign(b=expr)
    expected = pd.DataFrame({"a": [1, 2, 3], "b": pd.qcut(df["a"], 3)})
    tm.assert_frame_equal(result, expected)


def test_qcut():
    arr = np.random.default_rng(2).standard_normal(1000)

    # We store the bins as Index that have been
    # rounded to comparisons are a bit tricky.
    labels, _ = qcut(arr, 4, retbins=True)
    ex_bins = np.quantile(arr, [0, 0.25, 0.5, 0.75, 1.0])

    result = labels.categories.left.values
    assert np.allclose(result, ex_bins[:-1], atol=1e-2)

    result = labels.categories.right.values
    assert np.allclose(result, ex_bins[1:], atol=1e-2)

    ex_levels = cut(arr, ex_bins, include_lowest=True)
    tm.assert_categorical_equal(labels, ex_levels)

