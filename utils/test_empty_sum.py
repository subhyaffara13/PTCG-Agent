
def test_empty_sum():
    # https://github.com/pandas-dev/pandas/issues/18678
    df = DataFrame(
        {"A": Categorical(["a", "a", "b"], categories=["a", "b", "c"]), "B": [1, 2, 1]}
    )
    expected_idx = CategoricalIndex(["a", "b", "c"], name="A")

    # 0 by default
    result = df.groupby("A", observed=False).B.sum()
    expected = Series([3, 1, 0], expected_idx, name="B")
    tm.assert_series_equal(result, expected)

    # min_count=0
    result = df.groupby("A", observed=False).B.sum(min_count=0)
    expected = Series([3, 1, 0], expected_idx, name="B")
    tm.assert_series_equal(result, expected)

    # min_count=1
    result = df.groupby("A", observed=False).B.sum(min_count=1)
    expected = Series([3, 1, np.nan], expected_idx, name="B")
    tm.assert_series_equal(result, expected)

    # min_count>1
    result = df.groupby("A", observed=False).B.sum(min_count=2)
    expected = Series([3, np.nan, np.nan], expected_idx, name="B")
    tm.assert_series_equal(result, expected)

