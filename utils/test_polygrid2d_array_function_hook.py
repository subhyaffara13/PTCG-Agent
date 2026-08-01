
def test_polygrid2d_array_function_hook():
    x = ArrayFunctionInterceptor()
    y = ArrayFunctionInterceptor()
    c = ArrayFunctionInterceptor()
    result = np.polynomial.polynomial.polygrid2d(x, y, c)
    assert result == "intercepted"

