
def test_value_counts_all_na(sort, dropna, groupby_sort):
    # GH#59989
    df = DataFrame({"a": [2, 1, 1], "b": np.nan})
    gb = df.groupby("a", sort=groupby_sort)
    result = gb.value_counts(sort=sort, dropna=dropna)

    kwargs = {"levels": [[1, 2], [np.nan]], "names": ["a", "b"]}
    if dropna:
        data = []
        index = MultiIndex(codes=[[], []], **kwargs)
    elif not groupby_sort and not sort:
        data = [1, 2]
        index = MultiIndex(codes=[[1, 0], [0, 0]], **kwargs)
    else:
        data = [2, 1]
        index = MultiIndex(codes=[[0, 1], [0, 0]], **kwargs)
    expected = Series(data, index=index, dtype="int64", name="count")

    tm.assert_series_equal(result, expected)

