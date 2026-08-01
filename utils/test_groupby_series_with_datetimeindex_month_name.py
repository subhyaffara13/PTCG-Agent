
def test_groupby_series_with_datetimeindex_month_name():
    # GH 48509
    s = Series([0, 1, 0], index=date_range("2022-01-01", periods=3), name="jan")
    result = s.groupby(s).count()
    expected = Series([2, 1], name="jan")
    expected.index.name = "jan"
    tm.assert_series_equal(result, expected)

