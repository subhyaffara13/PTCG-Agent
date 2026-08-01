
def test_indices_concatenation_order():
    # GH 2808

    def f1(x):
        y = x[(x.b % 2) == 1] ** 2
        if y.empty:
            multiindex = MultiIndex(levels=[[]] * 2, codes=[[]] * 2, names=["b", "c"])
            res = DataFrame(columns=["a"], index=multiindex)
            return res
        else:
            y = y.set_index(["b", "c"])
            return y

    def f2(x):
        y = x[(x.b % 2) == 1] ** 2
        if y.empty:
            return DataFrame()
        else:
            y = y.set_index(["b", "c"])
            return y

    def f3(x):
        y = x[(x.b % 2) == 1] ** 2
        if y.empty:
            multiindex = MultiIndex(
                levels=[[]] * 2, codes=[[]] * 2, names=["foo", "bar"]
            )
            res = DataFrame(columns=["a", "b"], index=multiindex)
            return res
        else:
            return y

    df = DataFrame({"a": [1, 2, 2, 2], "b": range(4), "c": range(5, 9)})

    df2 = DataFrame({"a": [3, 2, 2, 2], "b": range(4), "c": range(5, 9)})

    # correct result
    result1 = df.groupby("a").apply(f1)
    result2 = df2.groupby("a").apply(f1)
    tm.assert_frame_equal(result1, result2)

    # should fail (not the same number of levels)
    msg = "Cannot concat indices that do not have the same number of levels"
    with pytest.raises(AssertionError, match=msg):
        df.groupby("a").apply(f2)
    with pytest.raises(AssertionError, match=msg):
        df2.groupby("a").apply(f2)

    # should fail (incorrect shape)
    with pytest.raises(AssertionError, match=msg):
        df.groupby("a").apply(f3)
    with pytest.raises(AssertionError, match=msg):
        df2.groupby("a").apply(f3)

