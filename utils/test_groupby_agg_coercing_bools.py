
def test_groupby_agg_coercing_bools():
    # issue 14873
    dat = DataFrame({"a": [1, 1, 2, 2], "b": [0, 1, 2, 3], "c": [None, None, 1, 1]})
    gp = dat.groupby("a")

    index = Index([1, 2], name="a")

    result = gp["b"].aggregate(lambda x: (x != 0).all())
    expected = Series([False, True], index=index, name="b")
    tm.assert_series_equal(result, expected)

    result = gp["c"].aggregate(lambda x: x.isnull().all())
    expected = Series([True, False], index=index, name="c")
    tm.assert_series_equal(result, expected)

