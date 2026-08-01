
def test_connectable_issue_example(conn, request):
    conn = request.getfixturevalue(conn)

    # This tests the example raised in issue
    # https://github.com/pandas-dev/pandas/issues/10104
    from sqlalchemy.engine import Engine

    def test_select(connection):
        query = "SELECT test_foo_data FROM test_foo_data"
        return sql.read_sql_query(query, con=connection)

    def test_append(connection, data):
        data.to_sql(name="test_foo_data", con=connection, if_exists="append")

    def test_connectable(conn):
        # https://github.com/sqlalchemy/sqlalchemy/commit/
        # 00b5c10846e800304caa86549ab9da373b42fa5d#r48323973
        foo_data = test_select(conn)
        test_append(conn, foo_data)

    def main(connectable):
        if isinstance(connectable, Engine):
            with connectable.connect() as conn:
                with conn.begin():
                    test_connectable(conn)
        else:
            test_connectable(connectable)

    assert (
        DataFrame({"test_foo_data": [0, 1, 2]}).to_sql(name="test_foo_data", con=conn)
        == 3
    )
    main(conn)

