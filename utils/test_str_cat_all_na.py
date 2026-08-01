
def test_str_cat_all_na(index_or_series, index_or_series2):
    # GH 24044
    box = index_or_series
    other = index_or_series2

    # check that all NaNs in caller / target work
    s = Index(["a", "b", "c", "d"])
    s = s if box == Index else Series(s, index=s)
    t = other([np.nan] * 4, dtype=object)
    # add index of s for alignment
    t = t if other == Index else Series(t, index=s)

    # all-NA target
    if box == Series:
        expected = Series([np.nan] * 4, index=s.index, dtype=s.dtype)
    else:  # box == Index
        # TODO: Strimg option, this should return string dtype
        expected = Index([np.nan] * 4, dtype=object)
    result = s.str.cat(t, join="left")
    tm.assert_equal(result, expected)

    # all-NA caller (only for Series)
    if other == Series:
        expected = Series([np.nan] * 4, dtype=object, index=t.index)
        result = t.str.cat(s, join="left")
        tm.assert_series_equal(result, expected)

