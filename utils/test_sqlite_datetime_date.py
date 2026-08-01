
def test_sqlite_datetime_date(sqlite_buildin):
    conn = sqlite_buildin
    df = DataFrame([date(2014, 1, 1), date(2014, 1, 2)], columns=["a"])
    assert df.to_sql(name="test_date", con=conn, index=False) == 2
    res = read_sql_query("SELECT * FROM test_date", conn)
    # comes back as strings
    tm.assert_frame_equal(res, df.astype(str))

