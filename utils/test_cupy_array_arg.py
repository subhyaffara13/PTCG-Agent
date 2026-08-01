
def test_cupy_array_arg():
    if not cupy:
        skip("CuPy not installed")

    f = lambdify([[x, y]], x*x + y, 'cupy')
    result = f(cupy.array([2.0, 1.0]))
    assert result == 5
    assert "cupy" in str(type(result))

