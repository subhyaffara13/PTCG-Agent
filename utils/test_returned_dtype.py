
def test_returned_dtype(disable_bottleneck, dtype, method, using_python_scalars):
    if dtype is None:
        pytest.skip("np.float128 not available")

    ser = Series(range(10), dtype=dtype)
    result = getattr(ser, method)()
    if using_python_scalars:
        if is_integer_dtype(dtype) and method in ["min", "max"]:
            assert isinstance(result, int)
        else:
            assert type(result) == float
    elif is_integer_dtype(dtype) and method not in ["min", "max"]:
        assert result.dtype == np.float64
    else:
        assert result.dtype == dtype

