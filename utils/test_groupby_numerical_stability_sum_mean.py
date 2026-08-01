
def test_groupby_numerical_stability_sum_mean(func, values):
    # GH#38778
    data = [1e16, 1e16, 97, 98, -5e15, -5e15, -5e15, -5e15]
    df = DataFrame({"group": [1, 2] * 4, "a": data, "b": data})
    result = getattr(df.groupby("group"), func)()
    expected = DataFrame({"a": values, "b": values}, index=Index([1, 2], name="group"))
    tm.assert_frame_equal(result, expected)

