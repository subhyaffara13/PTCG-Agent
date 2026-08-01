
def test_timedelta_assignment():
    # GH 8209
    s = Series([], dtype=object)
    s.loc["B"] = timedelta(1)
    expected = Series(Timedelta("1 days"), dtype="timedelta64[us]", index=["B"])
    tm.assert_series_equal(s, expected)

    s = s.reindex(s.index.insert(0, "A"))
    expected = Series(
        [np.nan, Timedelta("1 days")], dtype="timedelta64[us]", index=["A", "B"]
    )
    tm.assert_series_equal(s, expected)

    s.loc["A"] = timedelta(1)
    expected = Series(Timedelta("1 days"), dtype="timedelta64[us]", index=["A", "B"])
    tm.assert_series_equal(s, expected)

