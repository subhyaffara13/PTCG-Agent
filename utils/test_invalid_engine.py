
def test_invalid_engine():
    msg = "Invalid engine 'asdf' passed"
    with pytest.raises(KeyError, match=msg):
        pd.eval("x + y", local_dict={"x": 1, "y": 2}, engine="asdf")


def test_invalid_engine(df_compat, temp_file):
    msg = "engine must be one of 'pyarrow', 'fastparquet'"
    with pytest.raises(ValueError, match=msg):
        check_round_trip(df_compat, temp_file, "foo", "bar")


def test_invalid_engine(conn, request, test_frame1):
    if conn == "sqlite_buildin" or "adbc" in conn:
        request.applymarker(
            pytest.mark.xfail(
                reason="SQLiteDatabase/ADBCDatabase does not raise for bad engine"
            )
        )

    conn = request.getfixturevalue(conn)
    msg = "engine must be one of 'auto', 'sqlalchemy'"
    with pandasSQL_builder(conn) as pandasSQL:
        with pytest.raises(ValueError, match=msg):
            pandasSQL.to_sql(test_frame1, "test_frame1", engine="bad_engine")


def test_invalid_engine():
    with pytest.raises(ValueError, match="engine must be either 'numba' or 'cython'"):
        Series(range(1)).rolling(1).apply(lambda x: x, engine="foo")


def test_invalid_engine():
    # GH 48893
    ser = Series(range(1))
    out = ser.to_json()
    with pytest.raises(ValueError, match="The engine type foo"):
        read_json(out, engine="foo")

