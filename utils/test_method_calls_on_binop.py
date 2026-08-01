
def test_method_calls_on_binop():
    # GH 61175
    x = Series([1, 2, 3, 5])
    y = Series([2, 3, 4])

    # Method call on binary operation result
    result = pd.eval("(x + y).dropna()")
    expected = (x + y).dropna()
    tm.assert_series_equal(result, expected)

    # Test with other binary operations
    result = pd.eval("(x * y).dropna()")
    expected = (x * y).dropna()
    tm.assert_series_equal(result, expected)

    # Test with method chaining
    result = pd.eval("(x + y).dropna().reset_index(drop=True)")
    expected = (x + y).dropna().reset_index(drop=True)
    tm.assert_series_equal(result, expected)

