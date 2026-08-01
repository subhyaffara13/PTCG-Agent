
def test_insertion_method_on_conflict_update(conn, request):
    # GH 14553: Example in to_sql docstring
    conn = request.getfixturevalue(conn)

    from sqlalchemy.dialects.mysql import insert
    from sqlalchemy.engine import Engine
    from sqlalchemy.sql import text

    def insert_on_conflict(table, conn, keys, data_iter):
        data = [dict(zip(keys, row)) for row in data_iter]
        stmt = insert(table.table).values(data)
        stmt = stmt.on_duplicate_key_update(b=stmt.inserted.b, c=stmt.inserted.c)
        result = conn.execute(stmt)
        return result.rowcount

    create_sql = text(
        """
    CREATE TABLE test_insert_conflict (
        a INT PRIMARY KEY,
        b FLOAT,
        c VARCHAR(10)
    );
    """
    )
    if isinstance(conn, Engine):
        with conn.connect() as con:
            with con.begin():
                con.execute(create_sql)
    else:
        with conn.begin():
            conn.execute(create_sql)

    df = DataFrame([[1, 2.1, "a"]], columns=list("abc"))
    df.to_sql(name="test_insert_conflict", con=conn, if_exists="append", index=False)

    expected = DataFrame([[1, 3.2, "b"]], columns=list("abc"))
    inserted = expected.to_sql(
        name="test_insert_conflict",
        con=conn,
        index=False,
        if_exists="append",
        method=insert_on_conflict,
    )
    result = sql.read_sql_table("test_insert_conflict", conn)
    tm.assert_frame_equal(result, expected)
    assert inserted == 2

    # Cleanup
    with sql.SQLDatabase(conn, need_transaction=True) as pandasSQL:
        pandasSQL.drop_table("test_insert_conflict")

