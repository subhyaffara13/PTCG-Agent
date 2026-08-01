
def test_mi_indexing_list_nonexistent_raises():
    # GH 15452
    s = Series(range(4), index=MultiIndex.from_product([[1, 2], ["a", "b"]]))
    with pytest.raises(KeyError, match="\\['not' 'found'\\] not in index"):
        s.loc[["not", "found"]]

