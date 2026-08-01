
def test_notna_dtype(conn, request):
    if conn == "sqlite_str":
        pytest.skip("sqlite_str has no inspection system")

    conn_name = conn
    conn = request.getfixturevalue(conn)

    from sqlalchemy import (
        Boolean,
        DateTime,
        Float,
        Integer,
    )
    from sqlalchemy.schema import MetaData

    cols = {
        "Bool": Series([True, None]),
        "Date": Series([datetime(2012, 5, 1), None]),
        "Int": Series([1, None], dtype="object"),
        "Float": Series([1.1, None]),
    }
    df = DataFrame(cols)

    tbl = "notna_dtype_test"
    assert df.to_sql(name=tbl, con=conn) == 2
    _ = sql.read_sql_table(tbl, conn)
    meta = MetaData()
    meta.reflect(bind=conn)
    my_type = Integer if "mysql" in conn_name else Boolean
    col_dict = meta.tables[tbl].columns
    assert isinstance(col_dict["Bool"].type, my_type)
    assert isinstance(col_dict["Date"].type, DateTime)
    assert isinstance(col_dict["Int"].type, Integer)
    assert isinstance(col_dict["Float"].type, Float)

