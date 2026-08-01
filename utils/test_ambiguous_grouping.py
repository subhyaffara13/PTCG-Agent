
def test_ambiguous_grouping():
    # Test that groupby is not confused by groupings length equal to row count
    df = DataFrame({"a": [1, 1]})
    gb = df.groupby(np.array([1, 1], dtype=np.int64))
    result = gb.value_counts()
    expected = Series(
        [2], index=MultiIndex.from_tuples([[1, 1]], names=[None, "a"]), name="count"
    )
    tm.assert_series_equal(result, expected)

