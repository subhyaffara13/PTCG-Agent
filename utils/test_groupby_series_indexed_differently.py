
def test_groupby_series_indexed_differently():
    s1 = Series(
        [5.0, -9.0, 4.0, 100.0, -5.0, 55.0, 6.7],
        index=Index(["a", "b", "c", "d", "e", "f", "g"]),
    )
    s2 = Series(
        [1.0, 1.0, 4.0, 5.0, 5.0, 7.0], index=Index(["a", "b", "d", "f", "g", "h"])
    )

    grouped = s1.groupby(s2)
    agged = grouped.mean()
    exp = s1.groupby(s2.reindex(s1.index).get).mean()
    tm.assert_series_equal(agged, exp)

