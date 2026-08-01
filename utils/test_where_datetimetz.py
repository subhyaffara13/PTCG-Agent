
def test_where_datetimetz():
    # GH 15701
    timestamps = ["2016-12-31 12:00:04+00:00", "2016-12-31 12:00:04.010000+00:00"]
    ser = Series([Timestamp(t) for t in timestamps], dtype="datetime64[ns, UTC]")
    rs = ser.where(Series([False, True]))
    expected = Series([pd.NaT, ser[1]], dtype="datetime64[ns, UTC]")
    tm.assert_series_equal(rs, expected)

