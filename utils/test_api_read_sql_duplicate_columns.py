
def test_api_read_sql_duplicate_columns(conn, request):
    # GH#53117
    if "adbc" in conn:
        pa = pytest.importorskip("pyarrow")
        if not (
            Version(pa.__version__) >= Version("16.0")
            and conn in ["sqlite_adbc_conn", "postgresql_adbc_conn"]
        ):
            request.node.add_marker(
                pytest.mark.xfail(
                    reason="pyarrow->pandas throws ValueError", strict=True
                )
            )
    conn = request.getfixturevalue(conn)
    if sql.has_table("test_table", conn):
        with sql.SQLDatabase(conn, need_transaction=True) as pandasSQL:
            pandasSQL.drop_table("test_table")

    df = DataFrame({"a": [1, 2, 3], "b": [0.1, 0.2, 0.3], "c": 1})
    df.to_sql(name="test_table", con=conn, index=False)

    result = pd.read_sql("SELECT a, b, a +1 as a, c FROM test_table", conn)
    expected = DataFrame(
        [[1, 0.1, 2, 1], [2, 0.2, 3, 1], [3, 0.3, 4, 1]],
        columns=["a", "b", "a", "c"],
    )
    tm.assert_frame_equal(result, expected)

