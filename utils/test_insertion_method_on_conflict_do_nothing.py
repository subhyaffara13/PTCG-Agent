
def test_insertion_method_on_conflict_do_nothing(conn, request):
    # GH 15988: Example in to_sql docstring
    conn = request.getfixturevalue(conn)

    from sqlalchemy.dialects.postgresql import insert
    from sqlalchemy.engine import Engine
    from sqlalchemy.sql import text

    def insert_on_conflict(table, conn, keys, data_iter):
        data = [dict(zip(keys, row)) for row in data_iter]
        stmt = (
            insert(table.table)
            .values(data)
            .on_conflict_do_nothing(index_elements=["a"])
        )
        result = conn.execute(stmt)
        return result.rowcount

    create_sql = text(
        """
    CREATE TABLE test_insert_conflict (
        a  integer PRIMARY KEY,
        b  numeric,
        c  text
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

    expected = DataFrame([[1, 2.1, "a"]], columns=list("abc"))
    expected.to_sql(
        name="test_insert_conflict", con=conn, if_exists="append", index=False
    )

    df_insert = DataFrame([[1, 3.2, "b"]], columns=list("abc"))
    inserted = df_insert.to_sql(
        name="test_insert_conflict",
        con=conn,
        index=False,
        if_exists="append",
        method=insert_on_conflict,
    )
    result = sql.read_sql_table("test_insert_conflict", conn)
    tm.assert_frame_equal(result, expected)
    assert inserted == 0

    # Cleanup
    with sql.SQLDatabase(conn, need_transaction=True) as pandasSQL:
        pandasSQL.drop_table("test_insert_conflict")

