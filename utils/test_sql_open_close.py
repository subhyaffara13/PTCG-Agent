
def test_sql_open_close(temp_file, test_frame3):
    # Test if the IO in the database still work if the connection closed
    # between the writing and reading (as in many real situations).

    with contextlib.closing(sqlite3.connect(temp_file)) as conn:
        assert sql.to_sql(test_frame3, "test_frame3_legacy", conn, index=False) == 4

    with contextlib.closing(sqlite3.connect(temp_file)) as conn:
        result = sql.read_sql_query("SELECT * FROM test_frame3_legacy;", conn)

    tm.assert_frame_equal(test_frame3, result)

