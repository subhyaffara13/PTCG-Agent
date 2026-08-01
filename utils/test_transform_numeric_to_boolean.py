
def test_transform_numeric_to_boolean():
    # GH 16875
    # inconsistency in transforming boolean values
    expected = Series([True, True], name="A")

    df = DataFrame({"A": [1.1, 2.2], "B": [1, 2]})
    result = df.groupby("B").A.transform(lambda x: True)
    tm.assert_series_equal(result, expected)

    df = DataFrame({"A": [1, 2], "B": [1, 2]})
    result = df.groupby("B").A.transform(lambda x: True)
    tm.assert_series_equal(result, expected)

