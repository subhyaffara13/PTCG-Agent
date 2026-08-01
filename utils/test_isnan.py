
def test_isnan(dtype, string_list):
    if not hasattr(dtype, "na_object"):
        pytest.skip("no na support")
    sarr = np.array(string_list + [dtype.na_object], dtype=dtype)
    is_nan = isinstance(dtype.na_object, float) and np.isnan(dtype.na_object)
    bool_errors = 0
    try:
        bool(dtype.na_object)
    except TypeError:
        bool_errors = 1
    if is_nan or bool_errors:
        # isnan is only true when na_object is a NaN
        assert_array_equal(
            np.isnan(sarr),
            np.array([0] * len(string_list) + [1], dtype=np.bool),
        )
    else:
        assert not np.any(np.isnan(sarr))

