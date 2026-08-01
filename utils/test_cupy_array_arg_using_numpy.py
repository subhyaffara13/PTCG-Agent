
def test_cupy_array_arg_using_numpy():
    # numpy functions can be run on cupy arrays
    # unclear if we can "officially" support this,
    # depends on numpy __array_function__ support
    if not cupy:
        skip("CuPy not installed")

    f = lambdify([[x, y]], x*x + y, 'numpy')
    result = f(cupy.array([2.0, 1.0]))
    assert result == 5
    assert "cupy" in str(type(result))

