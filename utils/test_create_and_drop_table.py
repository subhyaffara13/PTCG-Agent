
def test_create_and_drop_table(sqlite_engine):
    conn = sqlite_engine
    temp_frame = DataFrame({"one": [1.0, 2.0, 3.0, 4.0], "two": [4.0, 3.0, 2.0, 1.0]})
    with sql.SQLDatabase(conn) as pandasSQL:
        with pandasSQL.run_transaction():
            assert pandasSQL.to_sql(temp_frame, "drop_test_frame") == 4

        assert pandasSQL.has_table("drop_test_frame")

        with pandasSQL.run_transaction():
            pandasSQL.drop_table("drop_test_frame")

        assert not pandasSQL.has_table("drop_test_frame")

