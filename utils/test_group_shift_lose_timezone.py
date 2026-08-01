
def test_group_shift_lose_timezone():
    # GH 30134
    now_dt = Timestamp.now("UTC").as_unit("ns")
    df = DataFrame({"a": [1, 1], "date": now_dt})
    result = df.groupby("a").shift(0).iloc[0]
    expected = Series({"date": now_dt}, name=result.name)
    tm.assert_series_equal(result, expected)

