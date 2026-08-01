
def test_bigint(conn, request):
    # int64 should be converted to BigInteger, GH7433
    conn = request.getfixturevalue(conn)
    df = DataFrame(data={"i64": [2**62]})
    assert df.to_sql(name="test_bigint", con=conn, index=False) == 1
    result = sql.read_sql_table("test_bigint", conn)

    tm.assert_frame_equal(df, result)

