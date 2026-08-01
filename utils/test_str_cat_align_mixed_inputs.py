
def test_str_cat_align_mixed_inputs(join_type):
    s = Series(["a", "b", "c", "d"])
    t = Series(["d", "a", "e", "b"], index=[3, 0, 4, 1])
    d = concat([t, t], axis=1)

    expected_outer = Series(["aaa", "bbb", "c--", "ddd", "-ee"])
    expected = expected_outer.loc[s.index.join(t.index, how=join_type)]

    # list of Series
    result = s.str.cat([t, t], join=join_type, na_rep="-")
    tm.assert_series_equal(result, expected)

    # DataFrame
    result = s.str.cat(d, join=join_type, na_rep="-")
    tm.assert_series_equal(result, expected)

    # mixed list of indexed/unindexed
    u = np.array(["A", "B", "C", "D"])
    expected_outer = Series(["aaA", "bbB", "c-C", "ddD", "-e-"])
    # joint index of rhs [t, u]; u will be forced have index of s
    rhs_idx = (
        t.index.intersection(s.index)
        if join_type == "inner"
        else t.index.union(s.index)
        if join_type == "outer"
        else t.index.append(s.index.difference(t.index))
    )

    expected = expected_outer.loc[s.index.join(rhs_idx, how=join_type)]
    result = s.str.cat([t, u], join=join_type, na_rep="-")
    tm.assert_series_equal(result, expected)

    with pytest.raises(TypeError, match="others must be Series,.*"):
        # nested lists are forbidden
        s.str.cat([t, list(u)], join=join_type)

    # errors for incorrect lengths
    rgx = r"If `others` contains arrays or lists \(or other list-likes.*"
    z = Series(["1", "2", "3"]).values

    # unindexed object of wrong length
    with pytest.raises(ValueError, match=rgx):
        s.str.cat(z, join=join_type)

    # unindexed object of wrong length in list
    with pytest.raises(ValueError, match=rgx):
        s.str.cat([t, z], join=join_type)

