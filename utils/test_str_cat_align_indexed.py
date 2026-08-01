
def test_str_cat_align_indexed(index_or_series, join_type):
    # https://github.com/pandas-dev/pandas/issues/18657
    box = index_or_series

    s = Series(["a", "b", "c", "d"], index=["a", "b", "c", "d"])
    t = Series(["D", "A", "E", "B"], index=["d", "a", "e", "b"])
    sa, ta = s.align(t, join=join_type)
    # result after manual alignment of inputs
    expected = sa.str.cat(ta, na_rep="-")

    if box == Index:
        s = Index(s)
        sa = Index(sa)
        expected = Index(expected)

    result = s.str.cat(t, join=join_type, na_rep="-")
    tm.assert_equal(result, expected)

