
def test_read_sql_dtype(conn, request, func, dtype_backend):
    # GH#50797
    conn = request.getfixturevalue(conn)
    table = "test"
    df = DataFrame({"a": [1, 2, 3], "b": 5})
    df.to_sql(name=table, con=conn, index=False, if_exists="replace")

    result = getattr(pd, func)(
        f"Select * from {table}",
        conn,
        dtype={"a": np.float64},
        dtype_backend=dtype_backend,
    )
    expected = DataFrame(
        {
            "a": Series([1, 2, 3], dtype=np.float64),
            "b": Series(
                [5, 5, 5],
                dtype="int64" if not dtype_backend == "numpy_nullable" else "Int64",
            ),
        }
    )
    tm.assert_frame_equal(result, expected)

