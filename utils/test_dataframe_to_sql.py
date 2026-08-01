
def test_dataframe_to_sql(conn, test_frame1, request):
    # GH 51086 if conn is sqlite_engine
    conn = request.getfixturevalue(conn)
    test_frame1.to_sql(name="test", con=conn, if_exists="append", index=False)

