
def test_default_date_load(conn, request):
    conn_name = conn
    if conn_name == "sqlite_str":
        pytest.skip("types tables not created in sqlite_str fixture")
    elif "sqlite" in conn_name:
        request.applymarker(
            pytest.mark.xfail(reason="sqlite does not read date properly")
        )

    conn = request.getfixturevalue(conn)
    df = sql.read_sql_table("types", conn)

    assert issubclass(df.DateCol.dtype.type, np.datetime64)

