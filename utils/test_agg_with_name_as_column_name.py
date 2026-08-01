
def test_agg_with_name_as_column_name():
    # GH 36212 - Column name is "name"
    data = {"name": ["foo", "bar"]}
    df = DataFrame(data)

    # result's name should be None
    result = df.agg({"name": "count"})
    expected = Series({"name": 2})
    tm.assert_series_equal(result, expected)

    # Check if name is still preserved when aggregating series instead
    result = df["name"].agg({"name": "count"})
    expected = Series({"name": 2}, name="name")
    tm.assert_series_equal(result, expected)

