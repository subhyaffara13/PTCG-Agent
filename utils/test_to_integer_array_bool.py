
def test_to_integer_array_bool(
    constructor, bool_values, int_values, target_dtype, expected_dtype, using_nan_is_na
):
    if not using_nan_is_na and np.isnan(bool_values[-1]):
        msg = "Cannot cast NaN value to Integer dtype"
        with pytest.raises(ValueError, match=msg):
            constructor(bool_values, dtype=target_dtype)
        with pytest.raises(ValueError, match=msg):
            pd.array(int_values, dtype=target_dtype)
        return

    result = constructor(bool_values, dtype=target_dtype)
    assert result.dtype == expected_dtype
    expected = pd.array(int_values, dtype=target_dtype)
    tm.assert_extension_array_equal(result, expected)

