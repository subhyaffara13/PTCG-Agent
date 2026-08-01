
def test_xsqlite_execute_fail(sqlite_buildin):
    create_sql = """
    CREATE TABLE test
    (
    a TEXT,
    b TEXT,
    c REAL,
    PRIMARY KEY (a, b)
    );
    """
    cur = sqlite_buildin.cursor()
    cur.execute(create_sql)

    with sql.pandasSQL_builder(sqlite_buildin) as pandas_sql:
        pandas_sql.execute("INSERT INTO test VALUES('foo', 'bar', 1.234)")
        pandas_sql.execute("INSERT INTO test VALUES('foo', 'baz', 2.567)")

        with pytest.raises(sql.DatabaseError, match="Execution failed on sql"):
            pandas_sql.execute("INSERT INTO test VALUES('foo', 'bar', 7)")

