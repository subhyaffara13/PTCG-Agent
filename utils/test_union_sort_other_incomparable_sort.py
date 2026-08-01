
def test_union_sort_other_incomparable_sort():
    idx = MultiIndex.from_product([[1, pd.Timestamp("2000")], ["a", "b"]])
    msg = "'<' not supported between instances of 'Timestamp' and 'int'"
    with pytest.raises(TypeError, match=msg):
        idx.union(idx[:1], sort=True)

