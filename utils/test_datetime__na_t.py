
def test_datetime_NaT(conn, request):
    conn_name = conn
    conn = request.getfixturevalue(conn)
    df = DataFrame(
        {"A": date_range("2013-01-01 09:00:00", periods=3), "B": np.arange(3.0)}
    )
    df.loc[1, "A"] = np.nan
    assert df.to_sql(name="test_datetime", con=conn, index=False) == 3

    # with read_table -> type information from schema used
    result = sql.read_sql_table("test_datetime", conn)
    expected = df[:]
    expected["A"] = expected["A"].astype("M8[us]")
    tm.assert_frame_equal(result, expected)

    # with read_sql -> no type information -> sqlite has no native
    result = sql.read_sql_query("SELECT * FROM test_datetime", conn)
    if "sqlite" in conn_name:
        assert isinstance(result.loc[0, "A"], str)
        result["A"] = to_datetime(result["A"], errors="coerce")

    tm.assert_frame_equal(result, expected)

