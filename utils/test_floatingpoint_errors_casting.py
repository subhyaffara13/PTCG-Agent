
def test_floatingpoint_errors_casting(dtype, value):
    dtype = np.dtype(dtype)
    for operation in check_operations(dtype, value):
        dtype = np.dtype(dtype)

        match = "invalid" if dtype.kind in 'iu' else "overflow"
        with pytest.warns(RuntimeWarning, match=match):
            operation()

        with np.errstate(all="raise"):
            with pytest.raises(FloatingPointError, match=match):
                operation()

