
def test_psycopg2_schema_support(postgresql_psycopg2_engine):
    conn = postgresql_psycopg2_engine

    # only test this for postgresql (schema's not supported in
    # mysql/sqlite)
    df = DataFrame({"col1": [1, 2], "col2": [0.1, 0.2], "col3": ["a", "n"]})

    # create a schema
    with conn.connect() as con:
        with con.begin():
            con.exec_driver_sql("DROP SCHEMA IF EXISTS other CASCADE;")
            con.exec_driver_sql("CREATE SCHEMA other;")

    # write dataframe to different schema's
    assert df.to_sql(name="test_schema_public", con=conn, index=False) == 2
    assert (
        df.to_sql(
            name="test_schema_public_explicit",
            con=conn,
            index=False,
            schema="public",
        )
        == 2
    )
    assert (
        df.to_sql(name="test_schema_other", con=conn, index=False, schema="other") == 2
    )

    # read dataframes back in
    res1 = sql.read_sql_table("test_schema_public", conn)
    tm.assert_frame_equal(df, res1)
    res2 = sql.read_sql_table("test_schema_public_explicit", conn)
    tm.assert_frame_equal(df, res2)
    res3 = sql.read_sql_table("test_schema_public_explicit", conn, schema="public")
    tm.assert_frame_equal(df, res3)
    res4 = sql.read_sql_table("test_schema_other", conn, schema="other")
    tm.assert_frame_equal(df, res4)
    msg = "Table test_schema_other not found"
    with pytest.raises(ValueError, match=msg):
        sql.read_sql_table("test_schema_other", conn, schema="public")

    # different if_exists options

    # create a schema
    with conn.connect() as con:
        with con.begin():
            con.exec_driver_sql("DROP SCHEMA IF EXISTS other CASCADE;")
            con.exec_driver_sql("CREATE SCHEMA other;")

    # write dataframe with different if_exists options
    assert (
        df.to_sql(name="test_schema_other", con=conn, schema="other", index=False) == 2
    )
    df.to_sql(
        name="test_schema_other",
        con=conn,
        schema="other",
        index=False,
        if_exists="replace",
    )
    assert (
        df.to_sql(
            name="test_schema_other",
            con=conn,
            schema="other",
            index=False,
            if_exists="append",
        )
        == 2
    )
    res = sql.read_sql_table("test_schema_other", conn, schema="other")
    tm.assert_frame_equal(concat([df, df], ignore_index=True), res)

