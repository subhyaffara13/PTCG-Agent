
def test_reindex_categorical():
    index = date_range("20000101", periods=3)

    # reindexing to an invalid Categorical
    s = Series(["a", "b", "c"], dtype="category")
    result = s.reindex(index)
    expected = Series(
        Categorical(values=[np.nan, np.nan, np.nan], categories=["a", "b", "c"])
    )
    expected.index = index
    tm.assert_series_equal(result, expected)

    # partial reindexing
    expected = Series(
        Categorical(values=["b", "c"], categories=["a", "b", "c"]), index=range(1, 3)
    )
    result = s.reindex([1, 2])
    tm.assert_series_equal(result, expected)

    expected = Series(
        Categorical(values=["c", np.nan], categories=["a", "b", "c"]), index=range(2, 4)
    )
    result = s.reindex([2, 3])
    tm.assert_series_equal(result, expected)

