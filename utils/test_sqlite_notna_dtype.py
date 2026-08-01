
def test_sqlite_notna_dtype(sqlite_buildin):
    conn = sqlite_buildin
    cols = {
        "Bool": Series([True, None]),
        "Date": Series([datetime(2012, 5, 1), None]),
        "Int": Series([1, None], dtype="object"),
        "Float": Series([1.1, None]),
    }
    df = DataFrame(cols)

    tbl = "notna_dtype_test"
    assert df.to_sql(name=tbl, con=conn) == 2

    assert get_sqlite_column_type(conn, tbl, "Bool") == "INTEGER"
    assert get_sqlite_column_type(conn, tbl, "Date") == "TIMESTAMP"
    assert get_sqlite_column_type(conn, tbl, "Int") == "INTEGER"
    assert get_sqlite_column_type(conn, tbl, "Float") == "REAL"

