
def test_str_transform_functions(method, exp):
    ser = pd.Series(["aBc dEF", None], dtype=ArrowDtype(pa.string()))
    result = getattr(ser.str, method)()
    expected = pd.Series([exp, None], dtype=ArrowDtype(pa.string()))
    tm.assert_series_equal(result, expected)

