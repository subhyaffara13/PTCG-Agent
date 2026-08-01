
def test_with_nested_series(datetime_series, op_name):
    # GH 2316 & GH52123
    # .agg with a reducer and a transform, what to do
    result = getattr(datetime_series, op_name)(
        lambda x: Series([x, x**2], index=["x", "x^2"])
    )
    if op_name == "apply":
        expected = DataFrame({"x": datetime_series, "x^2": datetime_series**2})
        tm.assert_frame_equal(result, expected)
    else:
        expected = Series([datetime_series, datetime_series**2], index=["x", "x^2"])
        tm.assert_series_equal(result, expected)

