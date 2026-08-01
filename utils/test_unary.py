
def test_unary(string_array, unicode_array, function_name):
    if function_name in ONLY_IN_NP_CHAR:
        func = getattr(np.char, function_name)
    else:
        func = getattr(np.strings, function_name)
    dtype = string_array.dtype
    sres = func(string_array)
    ures = func(unicode_array)
    if sres.dtype == StringDType():
        ures = ures.astype(StringDType())
    assert_array_equal(sres, ures)

    if not hasattr(dtype, "na_object"):
        return

    is_nan = np.isnan(np.array([dtype.na_object], dtype=dtype))[0]
    is_str = isinstance(dtype.na_object, str)
    na_arr = np.insert(string_array, 0, dtype.na_object)

    if function_name in UNIMPLEMENTED_VEC_STRING_FUNCTIONS:
        if not is_str:
            # to avoid these errors we'd need to add NA support to _vec_string
            with pytest.raises((ValueError, TypeError)):
                func(na_arr)
        elif function_name == "splitlines":
            assert func(na_arr)[0] == func(dtype.na_object)[()]
        else:
            assert func(na_arr)[0] == func(dtype.na_object)
        return
    if function_name == "str_len" and not is_str:
        # str_len always errors for any non-string null, even NA ones because
        # it has an integer result
        with pytest.raises(ValueError):
            func(na_arr)
        return
    if function_name in BOOL_OUTPUT_FUNCTIONS:
        if is_nan:
            assert func(na_arr)[0] is np.False_
        elif is_str:
            assert func(na_arr)[0] == func(dtype.na_object)
        else:
            with pytest.raises(ValueError):
                func(na_arr)
        return
    if not (is_nan or is_str):
        with pytest.raises(ValueError):
            func(na_arr)
        return
    res = func(na_arr)
    if is_nan and function_name in NAN_PRESERVING_FUNCTIONS:
        assert res[0] is dtype.na_object
    elif is_str:
        assert res[0] == func(dtype.na_object)

