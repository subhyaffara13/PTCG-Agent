
def test_transform_length(func):
    # GH 9697
    df = DataFrame({"col1": [1, 1, 2, 2], "col2": [1, 2, 3, np.nan]})
    if func is sum:
        expected = Series([3.0, 3.0, np.nan, np.nan])
    else:
        expected = Series([3.0] * 4)

    results = [
        df.groupby("col1").transform(func)["col2"],
        df.groupby("col1")["col2"].transform(func),
    ]
    for result in results:
        tm.assert_series_equal(result, expected, check_names=False)

