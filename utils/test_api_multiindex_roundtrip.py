
def test_api_multiindex_roundtrip(conn, request):
    conn = request.getfixturevalue(conn)
    if sql.has_table("test_multiindex_roundtrip", conn):
        with sql.SQLDatabase(conn, need_transaction=True) as pandasSQL:
            pandasSQL.drop_table("test_multiindex_roundtrip")

    df = DataFrame.from_records(
        [(1, 2.1, "line1"), (2, 1.5, "line2")],
        columns=["A", "B", "C"],
        index=["A", "B"],
    )

    df.to_sql(name="test_multiindex_roundtrip", con=conn)
    result = sql.read_sql_query(
        "SELECT * FROM test_multiindex_roundtrip", conn, index_col=["A", "B"]
    )
    tm.assert_frame_equal(df, result, check_index_type=True)

