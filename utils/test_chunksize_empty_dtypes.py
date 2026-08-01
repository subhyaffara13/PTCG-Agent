
def test_chunksize_empty_dtypes(conn, request):
    # GH#50245
    if "adbc" in conn:
        request.node.add_marker(
            pytest.mark.xfail(reason="chunksize argument NotImplemented with ADBC")
        )
    conn = request.getfixturevalue(conn)
    dtypes = {"a": "int64", "b": "object"}
    df = DataFrame(columns=["a", "b"]).astype(dtypes)
    expected = df.copy()
    df.to_sql(name="test", con=conn, index=False, if_exists="replace")

    for result in read_sql_query(
        "SELECT * FROM test",
        conn,
        dtype=dtypes,
        chunksize=1,
    ):
        tm.assert_frame_equal(result, expected)

