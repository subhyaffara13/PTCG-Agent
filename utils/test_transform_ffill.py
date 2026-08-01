
def test_transform_ffill():
    # GH 24211
    data = [["a", 0.0], ["a", float("nan")], ["b", 1.0], ["b", float("nan")]]
    df = DataFrame(data, columns=["key", "values"])
    result = df.groupby("key").transform("ffill")
    expected = DataFrame({"values": [0.0, 0.0, 1.0, 1.0]})
    tm.assert_frame_equal(result, expected)
    result = df.groupby("key")["values"].transform("ffill")
    expected = Series([0.0, 0.0, 1.0, 1.0], name="values")
    tm.assert_series_equal(result, expected)

