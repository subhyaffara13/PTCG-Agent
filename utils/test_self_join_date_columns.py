
def test_self_join_date_columns(postgresql_psycopg2_engine):
    # GH 44421
    conn = postgresql_psycopg2_engine
    from sqlalchemy.sql import text

    create_table = text(
        """
    CREATE TABLE person
    (
        id serial constraint person_pkey primary key,
        created_dt timestamp with time zone
    );

    INSERT INTO person
        VALUES (1, '2021-01-01T00:00:00Z');
    """
    )
    with conn.connect() as con:
        with con.begin():
            con.execute(create_table)

    sql_query = (
        'SELECT * FROM "person" AS p1 INNER JOIN "person" AS p2 ON p1.id = p2.id;'
    )
    result = pd.read_sql(sql_query, conn)
    expected = DataFrame(
        [[1, Timestamp("2021", tz="UTC")] * 2], columns=["id", "created_dt"] * 2
    )
    expected["created_dt"] = expected["created_dt"].astype("M8[us, UTC]")
    tm.assert_frame_equal(result, expected)

    # Cleanup
    with sql.SQLDatabase(conn, need_transaction=True) as pandasSQL:
        pandasSQL.drop_table("person")

