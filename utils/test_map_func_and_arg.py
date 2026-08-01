
def test_map_func_and_arg():
    # `arg`is considered a normal kwarg that should be passed to the function
    result = Series([1, 2]).map(lambda _, arg: arg, arg=3)
    expected = Series([3, 3])
    tm.assert_series_equal(result, expected)

