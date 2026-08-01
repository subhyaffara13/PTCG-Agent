
def test_map_simple_str_callables_same_as_astype(
    string_series, func, using_infer_string
):
    # test that we are evaluating row-by-row first
    # before vectorized evaluation
    result = string_series.map(func)
    expected = string_series.astype(str if not using_infer_string else "str")
    tm.assert_series_equal(result, expected)

