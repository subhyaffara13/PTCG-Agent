
def test_read_sql_dtype_backend_table(
    conn,
    request,
    string_storage,
    func,
    dtype_backend,
    dtype_backend_data,
    dtype_backend_expected,
):
    if "sqlite" in conn and "adbc" not in conn:
        request.applymarker(
            pytest.mark.xfail(
                reason=(
                    "SQLite actually returns proper boolean values via "
                    "read_sql_table, but before pytest refactor was skipped"
                )
            )
        )
    # GH#50048
    conn_name = conn
    conn = request.getfixturevalue(conn)
    table = "test"
    df = dtype_backend_data
    df.to_sql(name=table, con=conn, index=False, if_exists="replace")

    with pd.option_context("mode.string_storage", string_storage):
        result = getattr(pd, func)(table, conn, dtype_backend=dtype_backend)
        expected = dtype_backend_expected(string_storage, dtype_backend, conn_name)
    tm.assert_frame_equal(result, expected)

    if "adbc" in conn_name:
        # adbc does not support chunksize argument
        return

    with pd.option_context("mode.string_storage", string_storage):
        iterator = getattr(pd, func)(
            table,
            conn,
            dtype_backend=dtype_backend,
            chunksize=3,
        )
        expected = dtype_backend_expected(string_storage, dtype_backend, conn_name)
        for result in iterator:
            tm.assert_frame_equal(result, expected)

