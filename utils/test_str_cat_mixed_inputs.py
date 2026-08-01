
def test_str_cat_mixed_inputs(index_or_series):
    box = index_or_series
    s = Index(["a", "b", "c", "d"])
    s = s if box == Index else Series(s, index=s)

    t = Series(["A", "B", "C", "D"], index=s.values)
    d = concat([t, Series(s, index=s)], axis=1)

    expected = Index(["aAa", "bBb", "cCc", "dDd"])
    expected = expected if box == Index else Series(expected.values, index=s.values)

    # Series/Index with DataFrame
    result = s.str.cat(d)
    tm.assert_equal(result, expected)

    # Series/Index with two-dimensional ndarray
    result = s.str.cat(d.values)
    tm.assert_equal(result, expected)

    # Series/Index with list of Series
    result = s.str.cat([t, s])
    tm.assert_equal(result, expected)

    # Series/Index with mixed list of Series/array
    result = s.str.cat([t, s.values])
    tm.assert_equal(result, expected)

    # Series/Index with list of Series; different indexes
    t.index = ["b", "c", "d", "a"]
    expected = box(["aDa", "bAb", "cBc", "dCd"])
    expected = expected if box == Index else Series(expected.values, index=s.values)
    result = s.str.cat([t, s])
    tm.assert_equal(result, expected)

    # Series/Index with mixed list; different index
    result = s.str.cat([t, s.values])
    tm.assert_equal(result, expected)

    # Series/Index with DataFrame; different indexes
    d.index = ["b", "c", "d", "a"]
    expected = box(["aDd", "bAa", "cBb", "dCc"])
    expected = expected if box == Index else Series(expected.values, index=s.values)
    result = s.str.cat(d)
    tm.assert_equal(result, expected)

    # errors for incorrect lengths
    rgx = r"If `others` contains arrays or lists \(or other list-likes.*"
    z = Series(["1", "2", "3"])
    e = concat([z, z], axis=1)

    # two-dimensional ndarray
    with pytest.raises(ValueError, match=rgx):
        s.str.cat(e.values)

    # list of list-likes
    with pytest.raises(ValueError, match=rgx):
        s.str.cat([z.values, s.values])

    # mixed list of Series/list-like
    with pytest.raises(ValueError, match=rgx):
        s.str.cat([z.values, s])

    # errors for incorrect arguments in list-like
    rgx = "others must be Series, Index, DataFrame,.*"
    # make sure None/NaN do not crash checks in _get_series_list
    u = Series(["a", np.nan, "c", None])

    # mix of string and Series
    with pytest.raises(TypeError, match=rgx):
        s.str.cat([u, "u"])

    # DataFrame in list
    with pytest.raises(TypeError, match=rgx):
        s.str.cat([u, d])

    # 2-dim ndarray in list
    with pytest.raises(TypeError, match=rgx):
        s.str.cat([u, d.values])

    # nested lists
    with pytest.raises(TypeError, match=rgx):
        s.str.cat([u, [u, d]])

    # forbidden input type: set
    # GH 23009
    with pytest.raises(TypeError, match=rgx):
        s.str.cat(set(u))

    # forbidden input type: set in list
    # GH 23009
    with pytest.raises(TypeError, match=rgx):
        s.str.cat([u, set(u)])

    # other forbidden input type, e.g. int
    with pytest.raises(TypeError, match=rgx):
        s.str.cat(1)

    # nested list-likes
    with pytest.raises(TypeError, match=rgx):
        s.str.cat(iter([t.values, list(s)]))

