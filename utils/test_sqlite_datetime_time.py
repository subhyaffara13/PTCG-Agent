
def test_sqlite_datetime_time(tz_aware, sqlite_buildin):
    conn = sqlite_buildin
    # test support for datetime.time, GH #8341
    if not tz_aware:
        tz_times = [time(9, 0, 0), time(9, 1, 30)]
    else:
        tz_dt = date_range("2013-01-01 09:00:00", periods=2, tz="US/Pacific")
        tz_times = Series(tz_dt.to_pydatetime()).map(lambda dt: dt.timetz())

    df = DataFrame(tz_times, columns=["a"])

    assert df.to_sql(name="test_time", con=conn, index=False) == 2
    res = read_sql_query("SELECT * FROM test_time", conn)
    # comes back as strings
    expected = df.map(lambda _: _.strftime("%H:%M:%S.%f"))
    tm.assert_frame_equal(res, expected)

