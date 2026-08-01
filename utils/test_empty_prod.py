
def test_empty_prod():
    # https://github.com/pandas-dev/pandas/issues/18678
    df = DataFrame(
        {"A": Categorical(["a", "a", "b"], categories=["a", "b", "c"]), "B": [1, 2, 1]}
    )

    expected_idx = CategoricalIndex(["a", "b", "c"], name="A")

    # 1 by default
    result = df.groupby("A", observed=False).B.prod()
    expected = Series([2, 1, 1], expected_idx, name="B")
    tm.assert_series_equal(result, expected)

    # min_count=0
    result = df.groupby("A", observed=False).B.prod(min_count=0)
    expected = Series([2, 1, 1], expected_idx, name="B")
    tm.assert_series_equal(result, expected)

    # min_count=1
    result = df.groupby("A", observed=False).B.prod(min_count=1)
    expected = Series([2, 1, np.nan], expected_idx, name="B")
    tm.assert_series_equal(result, expected)

