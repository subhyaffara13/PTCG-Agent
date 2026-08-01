
def test_Float64_conversion():
    # GH#40729
    testseries = pd.Series(["1", "2", "3", "4"], dtype="object")
    result = testseries.astype(pd.Float64Dtype())

    expected = pd.Series([1.0, 2.0, 3.0, 4.0], dtype=pd.Float64Dtype())

    tm.assert_series_equal(result, expected)

