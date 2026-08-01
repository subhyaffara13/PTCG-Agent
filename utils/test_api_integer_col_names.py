
def test_api_integer_col_names(conn, request):
    conn = request.getfixturevalue(conn)
    df = DataFrame([[1, 2], [3, 4]], columns=[0, 1])
    sql.to_sql(df, "test_frame_integer_col_names", conn, if_exists="replace")

