
def test_dataframe_to_sql_empty(conn, test_frame1, request):
    if conn == "postgresql_adbc_conn" and not using_string_dtype():
        adbc_pg = pytest.importorskip("adbc_driver_postgresql")
        if Version(adbc_pg.__version__) < Version("1.11"):
            request.node.add_marker(
                pytest.mark.xfail(
                    reason=(
                        "postgres ADBC driver < 1.11 cannot insert index with null type"
                    ),
                )
            )

    # GH 51086 if conn is sqlite_engine
    conn = request.getfixturevalue(conn)
    empty_df = test_frame1.iloc[:0]
    empty_df.to_sql(name="test", con=conn, if_exists="append", index=False)

