
def test_api_to_sql_replace(conn, request, test_frame1):
    conn = request.getfixturevalue(conn)
    if sql.has_table("test_frame3", conn):
        with sql.SQLDatabase(conn, need_transaction=True) as pandasSQL:
            pandasSQL.drop_table("test_frame3")

    sql.to_sql(test_frame1, "test_frame3", conn, if_exists="fail")
    # Add to table again
    sql.to_sql(test_frame1, "test_frame3", conn, if_exists="replace")
    assert sql.has_table("test_frame3", conn)

    num_entries = len(test_frame1)
    num_rows = count_rows(conn, "test_frame3")

    assert num_rows == num_entries

