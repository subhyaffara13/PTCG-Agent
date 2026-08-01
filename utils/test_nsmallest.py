
def test_nsmallest():
    a = Series([1, 3, 5, 7, 2, 9, 0, 4, 6, 10])
    b = Series(list("a" * 5 + "b" * 5))
    gb = a.groupby(b)
    r = gb.nsmallest(3)
    e = Series(
        [1, 2, 3, 0, 4, 6],
        index=MultiIndex.from_arrays([list("aaabbb"), [0, 4, 1, 6, 7, 8]]),
    )
    tm.assert_series_equal(r, e)

    a = Series([1, 1, 3, 2, 0, 3, 3, 2, 1, 0])
    gb = a.groupby(b)
    e = Series(
        [0, 1, 1, 0, 1, 2],
        index=MultiIndex.from_arrays([list("aaabbb"), [4, 1, 0, 9, 8, 7]]),
    )
    tm.assert_series_equal(gb.nsmallest(3, keep="last"), e)

