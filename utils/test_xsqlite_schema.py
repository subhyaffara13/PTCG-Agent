
def test_xsqlite_schema(sqlite_buildin):
    frame = DataFrame(
        np.random.default_rng(2).standard_normal((10, 4)),
        columns=Index(list("ABCD")),
        index=date_range("2000-01-01", periods=10, freq="B"),
    )
    create_sql = sql.get_schema(frame, "test")
    lines = create_sql.splitlines()
    for line in lines:
        tokens = line.split(" ")
        if len(tokens) == 2 and tokens[0] == "A":
            assert tokens[1] == "DATETIME"

    create_sql = sql.get_schema(frame, "test", keys=["A", "B"])
    lines = create_sql.splitlines()
    assert 'PRIMARY KEY ("A", "B")' in create_sql
    cur = sqlite_buildin.cursor()
    cur.execute(create_sql)

