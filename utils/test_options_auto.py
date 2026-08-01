
def test_options_auto(df_compat, fp, pa, temp_file):
    # use the set option

    with pd.option_context("io.parquet.engine", "auto"):
        check_round_trip(df_compat, temp_file)


def test_options_auto(conn, request, test_frame1):
    # use the set option
    conn = request.getfixturevalue(conn)
    with pd.option_context("io.sql.engine", "auto"):
        with pandasSQL_builder(conn) as pandasSQL:
            with pandasSQL.run_transaction():
                assert pandasSQL.to_sql(test_frame1, "test_frame1") == 4
                assert pandasSQL.has_table("test_frame1")

        num_entries = len(test_frame1)
        num_rows = count_rows(conn, "test_frame1")
        assert num_rows == num_entries

