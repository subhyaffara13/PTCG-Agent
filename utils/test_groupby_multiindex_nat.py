
def test_groupby_multiindex_nat():
    # GH 9236
    values = [
        (pd.NaT, "a"),
        (datetime(2012, 1, 2), "a"),
        (datetime(2012, 1, 2), "b"),
        (datetime(2012, 1, 3), "a"),
    ]
    mi = MultiIndex.from_tuples(values, names=["date", None])
    ser = Series([3, 2, 2.5, 4], index=mi)

    result = ser.groupby(level=1).mean()
    expected = Series([3.0, 2.5], index=["a", "b"])
    tm.assert_series_equal(result, expected)

