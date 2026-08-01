
def test_sqlalchemy_default_type_conversion(conn, request):
    conn_name = conn
    if conn_name == "sqlite_str":
        pytest.skip("types tables not created in sqlite_str fixture")
    elif "mysql" in conn_name or "sqlite" in conn_name:
        request.applymarker(
            pytest.mark.xfail(reason="boolean dtype not inferred properly")
        )

    conn = request.getfixturevalue(conn)
    df = sql.read_sql_table("types", conn)

    assert issubclass(df.FloatCol.dtype.type, np.floating)
    assert issubclass(df.IntCol.dtype.type, np.integer)
    assert issubclass(df.BoolCol.dtype.type, np.bool_)

    # Int column with NA values stays as float
    assert issubclass(df.IntColWithNull.dtype.type, np.floating)
    # Bool column with NA values becomes object
    assert issubclass(df.BoolColWithNull.dtype.type, object)

