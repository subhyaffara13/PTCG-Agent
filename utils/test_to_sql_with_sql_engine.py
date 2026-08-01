
def test_to_sql_with_sql_engine(conn, request, test_frame1):
    """`to_sql` with the `engine` param"""
    # mostly copied from this class's `_to_sql()` method
    conn = request.getfixturevalue(conn)
    with pandasSQL_builder(conn) as pandasSQL:
        with pandasSQL.run_transaction():
            assert pandasSQL.to_sql(test_frame1, "test_frame1", engine="auto") == 4
            assert pandasSQL.has_table("test_frame1")

    num_entries = len(test_frame1)
    num_rows = count_rows(conn, "test_frame1")
    assert num_rows == num_entries

