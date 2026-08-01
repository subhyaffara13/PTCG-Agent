
def test_apply_reindex_values():
    # GH: 26209
    # reindexing from a single column of a groupby object with duplicate indices caused
    # a ValueError (cannot reindex from duplicate axis) in 0.24.2, the problem was
    # solved in #30679
    values = [1, 2, 3, 4]
    indices = [1, 1, 2, 2]
    df = DataFrame({"group": ["Group1", "Group2"] * 2, "value": values}, index=indices)
    expected = Series(values, index=indices, name="value")

    def reindex_helper(x):
        return x.reindex(np.arange(x.index.min(), x.index.max() + 1))

    # the following group by raised a ValueError
    result = df.groupby("group", group_keys=False).value.apply(reindex_helper)
    tm.assert_series_equal(expected, result)

