
def test_bigint_warning(sqlite_engine):
    conn = sqlite_engine
    # test no warning for BIGINT (to support int64) is raised (GH7433)
    df = DataFrame({"a": [1, 2]}, dtype="int64")
    assert df.to_sql(name="test_bigintwarning", con=conn, index=False) == 2

    with tm.assert_produces_warning(None):
        sql.read_sql_table("test_bigintwarning", conn)

