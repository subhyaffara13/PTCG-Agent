
def test_nan_numeric(conn, request):
    # NaNs in numeric float column
    conn = request.getfixturevalue(conn)
    df = DataFrame({"A": [0, 1, 2], "B": [0.2, np.nan, 5.6]})
    assert df.to_sql(name="test_nan", con=conn, index=False) == 3

    # with read_table
    result = sql.read_sql_table("test_nan", conn)
    tm.assert_frame_equal(result, df)

    # with read_sql
    result = sql.read_sql_query("SELECT * FROM test_nan", conn)
    tm.assert_frame_equal(result, df)

