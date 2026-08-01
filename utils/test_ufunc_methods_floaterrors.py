
def test_ufunc_methods_floaterrors(method):
    # adding inf and -inf (or log(-inf) creates an invalid float and warns
    arr = np.array([np.inf, 0, -np.inf])
    with np.errstate(all="warn"):
        with pytest.warns(RuntimeWarning, match="invalid value"):
            method(arr)

    arr = np.array([np.inf, 0, -np.inf])
    with np.errstate(all="raise"):
        with pytest.raises(FloatingPointError):
            method(arr)

