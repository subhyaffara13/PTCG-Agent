
def test_groupby_non_arithmetic_agg_int_like_precision(method, data):
    # GH#6620, GH#9311
    df = DataFrame({"a": [1, 1], "b": data})

    grouped = df.groupby("a")
    result = getattr(grouped, method)()
    if method == "count":
        expected_value = 2
    elif method == "first":
        expected_value = data[0]
    elif method == "last":
        expected_value = data[1]
    else:
        expected_value = getattr(df["b"], method)()
    expected = DataFrame({"b": [expected_value]}, index=pd.Index([1], name="a"))

    tm.assert_frame_equal(result, expected)

