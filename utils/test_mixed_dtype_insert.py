
def test_mixed_dtype_insert(conn, request):
    # see GH6509
    conn = request.getfixturevalue(conn)
    s1 = Series(2**25 + 1, dtype=np.int32)
    s2 = Series(0.0, dtype=np.float32)
    df = DataFrame({"s1": s1, "s2": s2})

    # write and read again
    assert df.to_sql(name="test_read_write", con=conn, index=False) == 1
    df2 = sql.read_sql_table("test_read_write", conn)

    tm.assert_frame_equal(df, df2, check_dtype=False, check_exact=True)

