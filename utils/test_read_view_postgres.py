
def test_read_view_postgres(conn, request):
    # GH 52969
    conn = request.getfixturevalue(conn)

    from sqlalchemy.engine import Engine
    from sqlalchemy.sql import text

    table_name = f"group_{uuid.uuid4().hex}"
    view_name = f"group_view_{uuid.uuid4().hex}"

    sql_stmt = text(
        f"""
    CREATE TABLE {table_name} (
        group_id INTEGER,
        name TEXT
    );
    INSERT INTO {table_name} VALUES
        (1, 'name');
    CREATE VIEW {view_name}
    AS
    SELECT * FROM {table_name};
    """
    )
    if isinstance(conn, Engine):
        with conn.connect() as con:
            with con.begin():
                con.execute(sql_stmt)
    else:
        with conn.begin():
            conn.execute(sql_stmt)
    result = read_sql_table(view_name, conn)
    expected = DataFrame({"group_id": [1], "name": "name"})
    tm.assert_frame_equal(result, expected)

