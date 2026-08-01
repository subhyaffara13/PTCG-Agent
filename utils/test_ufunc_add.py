
def test_ufunc_add(dtype, string_list, other_strings, use_out):
    arr1 = np.array(string_list, dtype=dtype)
    arr2 = np.array(other_strings, dtype=dtype)
    result = np.array([a + b for a, b in zip(arr1, arr2)], dtype=dtype)

    if use_out:
        res = np.add(arr1, arr2, out=arr1)
    else:
        res = np.add(arr1, arr2)

    assert_array_equal(res, result)

    if not hasattr(dtype, "na_object"):
        return

    is_nan = isinstance(dtype.na_object, float) and np.isnan(dtype.na_object)
    is_str = isinstance(dtype.na_object, str)
    bool_errors = 0
    try:
        bool(dtype.na_object)
    except TypeError:
        bool_errors = 1

    arr1 = np.array([dtype.na_object] + string_list, dtype=dtype)
    arr2 = np.array(other_strings + [dtype.na_object], dtype=dtype)

    if is_nan or bool_errors or is_str:
        res = np.add(arr1, arr2)
        assert_array_equal(res[1:-1], arr1[1:-1] + arr2[1:-1])
        if not is_str:
            assert res[0] is dtype.na_object and res[-1] is dtype.na_object
        else:
            assert res[0] == dtype.na_object + arr2[0]
            assert res[-1] == arr1[-1] + dtype.na_object
    else:
        with pytest.raises(ValueError):
            np.add(arr1, arr2)

