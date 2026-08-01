
def test_multiindex_unique():
    mi = MultiIndex.from_tuples([(118, 472), (236, 118), (51, 204), (102, 51)])
    assert mi.is_unique is True

    result = hash_pandas_object(mi)
    assert result.is_unique is True

