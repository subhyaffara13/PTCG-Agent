
def test_default_type_conversion(conn, request):
    conn_name = conn
    if conn_name == "sqlite_buildin_types":
        request.applymarker(
            pytest.mark.xfail(
                reason="sqlite_buildin connection does not implement read_sql_table"
            )
        )

    conn = request.getfixturevalue(conn)
    df = sql.read_sql_table("types", conn)

    assert issubclass(df.FloatCol.dtype.type, np.floating)
    assert issubclass(df.IntCol.dtype.type, np.integer)

    # MySQL/sqlite has no real BOOL type
    if "postgresql" in conn_name:
        assert issubclass(df.BoolCol.dtype.type, np.bool_)
    else:
        assert issubclass(df.BoolCol.dtype.type, np.integer)

    # Int column with NA values stays as float
    assert issubclass(df.IntColWithNull.dtype.type, np.floating)

    # Bool column with NA = int column with NA values => becomes float
    if "postgresql" in conn_name:
        assert issubclass(df.BoolColWithNull.dtype.type, object)
    else:
        assert issubclass(df.BoolColWithNull.dtype.type, np.floating)

