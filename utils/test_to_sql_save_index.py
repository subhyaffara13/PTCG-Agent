
def test_to_sql_save_index(conn, request):
    if "adbc" in conn:
        request.node.add_marker(
            pytest.mark.xfail(
                reason="ADBC implementation does not create index", strict=True
            )
        )
    conn_name = conn
    conn = request.getfixturevalue(conn)
    df = DataFrame.from_records(
        [(1, 2.1, "line1"), (2, 1.5, "line2")], columns=["A", "B", "C"], index=["A"]
    )

    tbl_name = "test_to_sql_saves_index"
    with pandasSQL_builder(conn) as pandasSQL:
        with pandasSQL.run_transaction():
            assert pandasSQL.to_sql(df, tbl_name) == 2

    if conn_name in {"sqlite_buildin", "sqlite_str"}:
        ixs = sql.read_sql_query(
            "SELECT * FROM sqlite_master WHERE type = 'index' "
            f"AND tbl_name = '{tbl_name}'",
            conn,
        )
        ix_cols = []
        for ix_name in ixs.name:
            ix_info = sql.read_sql_query(f"PRAGMA index_info({ix_name})", conn)
            ix_cols.append(ix_info.name.tolist())
    else:
        from sqlalchemy import inspect

        insp = inspect(conn)

        ixs = insp.get_indexes(tbl_name)
        ix_cols = [i["column_names"] for i in ixs]

    assert ix_cols == [["A"]]

