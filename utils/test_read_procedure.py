
def test_read_procedure(conn, request):
    conn = request.getfixturevalue(conn)

    # GH 7324
    # Although it is more an api test, it is added to the
    # mysql tests as sqlite does not have stored procedures
    from sqlalchemy import text
    from sqlalchemy.engine import Engine

    df = DataFrame({"a": [1, 2, 3], "b": [0.1, 0.2, 0.3]})
    df.to_sql(name="test_frame", con=conn, index=False)

    proc = """DROP PROCEDURE IF EXISTS get_testdb;

    CREATE PROCEDURE get_testdb ()

    BEGIN
        SELECT * FROM test_frame;
    END"""
    proc = text(proc)
    if isinstance(conn, Engine):
        with conn.connect() as engine_conn:
            with engine_conn.begin():
                engine_conn.execute(proc)
    else:
        with conn.begin():
            conn.execute(proc)

    res1 = sql.read_sql_query("CALL get_testdb();", conn)
    tm.assert_frame_equal(df, res1)

    # test delegation to read_sql_query
    res2 = sql.read_sql("CALL get_testdb();", conn)
    tm.assert_frame_equal(df, res2)

