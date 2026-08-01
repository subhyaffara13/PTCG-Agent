
def test_setitem_ambiguous_keyerror(indexer_sl):
    s = Series(range(10), index=list(range(0, 20, 2)))

    # equivalent of an append
    s2 = s.copy()
    indexer_sl(s2)[1] = 5
    expected = concat([s, Series([5], index=[1])])
    tm.assert_series_equal(s2, expected)

