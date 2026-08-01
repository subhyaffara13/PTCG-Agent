
def test_drop_table(conn, request):
    if conn == "sqlite_str":
        pytest.skip("sqlite_str has no inspection system")

    conn = request.getfixturevalue(conn)

    from sqlalchemy import inspect

    temp_frame = DataFrame({"one": [1.0, 2.0, 3.0, 4.0], "two": [4.0, 3.0, 2.0, 1.0]})
    with sql.SQLDatabase(conn) as pandasSQL:
        with pandasSQL.run_transaction():
            assert pandasSQL.to_sql(temp_frame, "temp_frame") == 4

        insp = inspect(conn)
        assert insp.has_table("temp_frame")

        with pandasSQL.run_transaction():
            pandasSQL.drop_table("temp_frame")
        try:
            insp.clear_cache()  # needed with SQLAlchemy 2.0, unavailable prior
        except AttributeError:
            pass
        assert not insp.has_table("temp_frame")

