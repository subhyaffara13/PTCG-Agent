
def test_ufunc_multiply(dtype, string_list, other, other_dtype, use_out):
    """Test the two-argument ufuncs match python builtin behavior."""
    arr = np.array(string_list, dtype=dtype)
    if other_dtype is not None:
        other_dtype = np.dtype(other_dtype)
    try:
        len(other)
        result = [s * o for s, o in zip(string_list, other)]
        other = np.array(other)
        if other_dtype is not None:
            other = other.astype(other_dtype)
    except TypeError:
        if other_dtype is not None:
            other = other_dtype.type(other)
        result = [s * other for s in string_list]

    if use_out:
        arr_cache = arr.copy()
        lres = np.multiply(arr, other, out=arr)
        assert_array_equal(lres, result)
        arr[:] = arr_cache
        assert lres is arr
        arr *= other
        assert_array_equal(arr, result)
        arr[:] = arr_cache
        rres = np.multiply(other, arr, out=arr)
        assert rres is arr
        assert_array_equal(rres, result)
    else:
        lres = arr * other
        assert_array_equal(lres, result)
        rres = other * arr
        assert_array_equal(rres, result)

    if not hasattr(dtype, "na_object"):
        return

    is_nan = np.isnan(np.array([dtype.na_object], dtype=dtype))[0]
    is_str = isinstance(dtype.na_object, str)
    bool_errors = 0
    try:
        bool(dtype.na_object)
    except TypeError:
        bool_errors = 1

    arr = np.array(string_list + [dtype.na_object], dtype=dtype)

    try:
        len(other)
        other = np.append(other, 3)
        if other_dtype is not None:
            other = other.astype(other_dtype)
    except TypeError:
        pass

    if is_nan or bool_errors or is_str:
        for res in [arr * other, other * arr]:
            assert_array_equal(res[:-1], result)
            if not is_str:
                assert res[-1] is dtype.na_object
            else:
                try:
                    assert res[-1] == dtype.na_object * other[-1]
                except (IndexError, TypeError):
                    assert res[-1] == dtype.na_object * other
    else:
        with pytest.raises(TypeError):
            arr * other
        with pytest.raises(TypeError):
            other * arr

