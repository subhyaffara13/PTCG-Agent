
def test_groupby_transform_timezone_column(func):
    # GH 24198
    ts = pd.to_datetime("now", utc=True).tz_convert("Asia/Singapore")
    result = DataFrame({"end_time": [ts], "id": [1]})
    result["max_end_time"] = result.groupby("id").end_time.transform(func)
    expected = DataFrame([[ts, 1, ts]], columns=["end_time", "id", "max_end_time"])
    tm.assert_frame_equal(result, expected)

