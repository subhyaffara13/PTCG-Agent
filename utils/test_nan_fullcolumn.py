
def test_nan_fullcolumn(conn, request):
    # full NaN column (numeric float column)
    conn = request.getfixturevalue(conn)
    df = DataFrame({"A": [0, 1, 2], "B": [np.nan, np.nan, np.nan]})
    assert df.to_sql(name="test_nan", con=conn, index=False) == 3

    # with read_table
    result = sql.read_sql_table("test_nan", conn)
    tm.assert_frame_equal(result, df)

    # with read_sql -> not type info from table -> stays None
    df["B"] = df["B"].astype("object")
    df["B"] = None
    result = sql.read_sql_query("SELECT * FROM test_nan", conn)
    tm.assert_frame_equal(result, df)

