
def test_warning_case_insensitive_table_name(conn, request, test_frame1):
    conn_name = conn
    if conn_name == "sqlite_buildin" or "adbc" in conn_name:
        request.applymarker(pytest.mark.xfail(reason="Does not raise warning"))

    conn = request.getfixturevalue(conn)
    # see gh-7815
    with tm.assert_produces_warning(
        UserWarning,
        match=(
            r"The provided table name 'TABLE1' is not found exactly as such in "
            r"the database after writing the table, possibly due to case "
            r"sensitivity issues. Consider using lower case table names."
        ),
    ):
        with sql.SQLDatabase(conn) as db:
            db.check_case_sensitive("TABLE1", "")

    # Test that the warning is certainly NOT triggered in a normal case.
    with tm.assert_produces_warning(None):
        test_frame1.to_sql(name="CaseSensitive", con=conn)

