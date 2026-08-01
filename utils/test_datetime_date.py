
def test_datetime_date(conn, request):
    # test support for datetime.date
    conn = request.getfixturevalue(conn)
    df = DataFrame([date(2014, 1, 1), date(2014, 1, 2)], columns=["a"])
    assert df.to_sql(name="test_date", con=conn, index=False) == 2
    res = read_sql_table("test_date", conn)
    result = res["a"]
    expected = to_datetime(df["a"])
    # comes back as datetime64
    tm.assert_series_equal(result, expected)

