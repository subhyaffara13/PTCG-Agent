
def test_binary(string_array, unicode_array, function_name, args):
    if function_name in ONLY_IN_NP_CHAR:
        func = getattr(np.char, function_name)
    else:
        func = getattr(np.strings, function_name)
    sres = call_func(func, args, string_array)
    ures = call_func(func, args, unicode_array, sanitize=False)
    if not isinstance(sres, tuple) and sres.dtype == StringDType():
        ures = ures.astype(StringDType())
    assert_array_equal(sres, ures)

    dtype = string_array.dtype
    if function_name not in SUPPORTS_NULLS or not hasattr(dtype, "na_object"):
        return

    na_arr = np.insert(string_array, 0, dtype.na_object)
    is_nan = np.isnan(np.array([dtype.na_object], dtype=dtype))[0]
    is_str = isinstance(dtype.na_object, str)
    should_error = not (is_nan or is_str)

    if (
        (function_name in NULLS_ALWAYS_ERROR and not is_str)
        or (function_name in PASSES_THROUGH_NAN_NULLS and should_error)
        or (function_name in NULLS_ARE_FALSEY and should_error)
    ):
        with pytest.raises((ValueError, TypeError)):
            call_func(func, args, na_arr)
        return

    res = call_func(func, args, na_arr)

    if is_str:
        assert res[0] == call_func(func, args, na_arr[:1])
    elif function_name in NULLS_ARE_FALSEY:
        assert res[0] is np.False_
    elif function_name in PASSES_THROUGH_NAN_NULLS:
        assert res[0] is dtype.na_object
    else:
        # shouldn't ever get here
        assert 0

