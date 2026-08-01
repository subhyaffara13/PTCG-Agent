
def test_transaction_rollback(conn, request):
    conn_name = conn
    conn = request.getfixturevalue(conn)
    with pandasSQL_builder(conn) as pandasSQL:
        with pandasSQL.run_transaction() as trans:
            stmt = "CREATE TABLE test_trans (A INT, B TEXT)"
            if "adbc" in conn_name or isinstance(pandasSQL, SQLiteDatabase):
                trans.execute(stmt)
            else:
                from sqlalchemy import text

                stmt = text(stmt)
                trans.execute(stmt)

        class DummyException(Exception):
            pass

        # Make sure when transaction is rolled back, no rows get inserted
        ins_sql = "INSERT INTO test_trans (A,B) VALUES (1, 'blah')"
        if isinstance(pandasSQL, SQLDatabase):
            from sqlalchemy import text

            ins_sql = text(ins_sql)
        try:
            with pandasSQL.run_transaction() as trans:
                trans.execute(ins_sql)
                raise DummyException("error")
        except DummyException:
            # ignore raised exception
            pass
        with pandasSQL.run_transaction():
            res = pandasSQL.read_query("SELECT * FROM test_trans")
        assert len(res) == 0

        # Make sure when transaction is committed, rows do get inserted
        with pandasSQL.run_transaction() as trans:
            trans.execute(ins_sql)
            res2 = pandasSQL.read_query("SELECT * FROM test_trans")
        assert len(res2) == 1

