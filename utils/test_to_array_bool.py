
def test_to_array_bool(bool_values, values, target_dtype, expected_dtype):
    result = pd.array(bool_values, dtype=target_dtype)
    assert result.dtype == expected_dtype
    expected = pd.array(values, dtype=target_dtype)
    tm.assert_extension_array_equal(result, expected)

