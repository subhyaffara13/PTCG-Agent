
def test_naive_datetimeindex_roundtrip(conn, request):
    # GH 23510
    # Ensure that a naive DatetimeIndex isn't converted to UTC
    conn = request.getfixturevalue(conn)
    dates = date_range("2018-01-01", periods=5, freq="6h", unit="us")._with_freq(None)
    expected = DataFrame({"nums": range(5)}, index=dates)
    assert expected.to_sql(name="foo_table", con=conn, index_label="info_date") == 5
    result = sql.read_sql_table("foo_table", conn, index_col="info_date")
    # result index with gain a name from a set_index operation; expected
    tm.assert_frame_equal(result, expected, check_names=False)

