
def test_polyval2d_array_function_hook():
    x = ArrayFunctionInterceptor()
    y = ArrayFunctionInterceptor()
    c = ArrayFunctionInterceptor()
    result = np.polynomial.polynomial.polyval2d(x, y, c)
    assert result == "intercepted"

