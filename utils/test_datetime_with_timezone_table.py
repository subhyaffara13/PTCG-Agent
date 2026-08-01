
def test_datetime_with_timezone_table(conn, request):
    conn = request.getfixturevalue(conn)
    expected = create_and_load_postgres_datetz(conn)
    result = sql.read_sql_table("datetz", conn)

    exp_frame = expected.to_frame()
    tm.assert_frame_equal(result, exp_frame)

