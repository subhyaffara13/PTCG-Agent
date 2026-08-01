
def test_delete_rows_success(conn_name, test_frame1, request):
    table_name = "temp_delete_rows_frame"
    conn = request.getfixturevalue(conn_name)

    with pandasSQL_builder(conn) as pandasSQL:
        with pandasSQL.run_transaction():
            assert pandasSQL.to_sql(test_frame1, table_name) == test_frame1.shape[0]

        with pandasSQL.run_transaction():
            assert pandasSQL.delete_rows(table_name) is None

        assert count_rows(conn, table_name) == 0
        assert pandasSQL.has_table(table_name)

