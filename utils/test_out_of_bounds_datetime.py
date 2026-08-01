
def test_out_of_bounds_datetime(conn, request):
    # GH 26761
    conn = request.getfixturevalue(conn)
    data = DataFrame({"date": datetime(9999, 1, 1)}, index=[0])
    assert data.to_sql(name="test_datetime_obb", con=conn, index=False) == 1
    result = sql.read_sql_table("test_datetime_obb", conn)
    expected = DataFrame(
        np.array([datetime(9999, 1, 1)], dtype="M8[us]"), columns=["date"]
    )
    tm.assert_frame_equal(result, expected)

