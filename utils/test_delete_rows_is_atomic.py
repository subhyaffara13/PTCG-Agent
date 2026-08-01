
def test_delete_rows_is_atomic(conn_name, request):
    sqlalchemy = pytest.importorskip("sqlalchemy")

    table_name = "temp_delete_rows_atomic_frame"
    table_stmt = f"CREATE TABLE {table_name} (a INTEGER, b INTEGER UNIQUE NOT NULL)"

    if conn_name != "sqlite_buildin" and "adbc" not in conn_name:
        table_stmt = sqlalchemy.text(table_stmt)

    # setting dtype is mandatory for adbc related tests
    original_df = DataFrame({"a": [1, 2], "b": [3, 4]}, dtype="int32")
    replacing_df = DataFrame({"a": [5, 6, 7], "b": [8, 8, 8]}, dtype="int32")

    conn = request.getfixturevalue(conn_name)
    with pandasSQL_builder(conn) as pandasSQL:
        with pandasSQL.run_transaction() as cur:
            cur.execute(table_stmt)

        with pandasSQL.run_transaction():
            pandasSQL.to_sql(original_df, table_name, if_exists="append", index=False)

        # inserting duplicated values in a UNIQUE constraint column
        with pytest.raises(pd.errors.DatabaseError):
            with pandasSQL.run_transaction():
                pandasSQL.to_sql(
                    replacing_df, table_name, if_exists="delete_rows", index=False
                )

        # failed "delete_rows" is rolled back preserving original data
        with pandasSQL.run_transaction():
            result_df = pandasSQL.read_query(
                f"SELECT * FROM {table_name}", dtype="int32"
            )
            tm.assert_frame_equal(result_df, original_df)

