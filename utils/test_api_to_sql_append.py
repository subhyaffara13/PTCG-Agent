
def test_api_to_sql_append(conn, request, test_frame1):
    conn = request.getfixturevalue(conn)
    if sql.has_table("test_frame4", conn):
        with sql.SQLDatabase(conn, need_transaction=True) as pandasSQL:
            pandasSQL.drop_table("test_frame4")

    assert sql.to_sql(test_frame1, "test_frame4", conn, if_exists="fail") == 4

    # Add to table again
    assert sql.to_sql(test_frame1, "test_frame4", conn, if_exists="append") == 4
    assert sql.has_table("test_frame4", conn)

    num_entries = 2 * len(test_frame1)
    num_rows = count_rows(conn, "test_frame4")

    assert num_rows == num_entries

