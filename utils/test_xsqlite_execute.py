
def test_xsqlite_execute(sqlite_buildin):
    frame = DataFrame(
        np.random.default_rng(2).standard_normal((10, 4)),
        columns=Index(list("ABCD")),
        index=date_range("2000-01-01", periods=10, freq="B"),
    )
    create_sql = sql.get_schema(frame, "test")
    cur = sqlite_buildin.cursor()
    cur.execute(create_sql)
    ins = "INSERT INTO test VALUES (?, ?, ?, ?)"

    row = frame.iloc[0]
    with sql.pandasSQL_builder(sqlite_buildin) as pandas_sql:
        pandas_sql.execute(ins, tuple(row))
    sqlite_buildin.commit()

    result = sql.read_sql("select * from test", sqlite_buildin)
    result.index = frame.index[:1]
    tm.assert_frame_equal(result, frame[:1])

