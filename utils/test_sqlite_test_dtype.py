
def test_sqlite_test_dtype(sqlite_buildin):
    conn = sqlite_buildin
    cols = ["A", "B"]
    data = [(0.8, True), (0.9, None)]
    df = DataFrame(data, columns=cols)
    assert df.to_sql(name="dtype_test", con=conn) == 2
    assert df.to_sql(name="dtype_test2", con=conn, dtype={"B": "STRING"}) == 2

    # sqlite stores Boolean values as INTEGER
    assert get_sqlite_column_type(conn, "dtype_test", "B") == "INTEGER"

    assert get_sqlite_column_type(conn, "dtype_test2", "B") == "STRING"
    msg = r"B \(<class 'bool'>\) not a string"
    with pytest.raises(ValueError, match=msg):
        df.to_sql(name="error", con=conn, dtype={"B": bool})

    # single dtype
    assert df.to_sql(name="single_dtype_test", con=conn, dtype="STRING") == 2
    assert get_sqlite_column_type(conn, "single_dtype_test", "A") == "STRING"
    assert get_sqlite_column_type(conn, "single_dtype_test", "B") == "STRING"

