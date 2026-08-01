
def test_ufuncs_minmax(string_list, ufunc_name, func, use_out):
    """Test that the min/max ufuncs match Python builtin min/max behavior."""
    arr = np.array(string_list, dtype="T")
    uarr = np.array(string_list, dtype=str)
    res = np.array(func(string_list), dtype="T")
    assert_array_equal(getattr(arr, ufunc_name)(), res)

    ufunc = getattr(np, ufunc_name + "imum")

    if use_out:
        res = ufunc(arr, arr, out=arr)
    else:
        res = ufunc(arr, arr)

    assert_array_equal(uarr, res)
    assert_array_equal(getattr(arr, ufunc_name)(), func(string_list))

