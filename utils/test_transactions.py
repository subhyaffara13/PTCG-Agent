
def test_transactions(conn, request):
    conn_name = conn
    conn = request.getfixturevalue(conn)

    stmt = "CREATE TABLE test_trans (A INT, B TEXT)"
    if conn_name != "sqlite_buildin" and "adbc" not in conn_name:
        from sqlalchemy import text

        stmt = text(stmt)

    with pandasSQL_builder(conn) as pandasSQL:
        with pandasSQL.run_transaction() as trans:
            trans.execute(stmt)

