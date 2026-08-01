
def test_options_sqlalchemy(conn, request, test_frame1):
    # use the set option
    conn = request.getfixturevalue(conn)
    with pd.option_context("io.sql.engine", "sqlalchemy"):
        with pandasSQL_builder(conn) as pandasSQL:
            with pandasSQL.run_transaction():
                assert pandasSQL.to_sql(test_frame1, "test_frame1") == 4
                assert pandasSQL.has_table("test_frame1")

        num_entries = len(test_frame1)
        num_rows = count_rows(conn, "test_frame1")
        assert num_rows == num_entries

