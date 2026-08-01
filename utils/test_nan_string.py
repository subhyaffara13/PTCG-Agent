
def test_nan_string(conn, request):
    # NaNs in string column
    conn = request.getfixturevalue(conn)
    df = DataFrame({"A": [0, 1, 2], "B": ["a", "b", np.nan]})
    assert df.to_sql(name="test_nan", con=conn, index=False) == 3

    # NaNs are coming back as None
    df.loc[2, "B"] = None

    # with read_table
    result = sql.read_sql_table("test_nan", conn)
    tm.assert_frame_equal(result, df)

    # with read_sql
    result = sql.read_sql_query("SELECT * FROM test_nan", conn)
    tm.assert_frame_equal(result, df)

