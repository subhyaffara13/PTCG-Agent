
def test_to_integer_array(values, to_dtype, result_dtype, using_nan_is_na):
    # convert existing arrays to IntegerArrays
    if not using_nan_is_na and np.isnan(values[-1]):
        msg = "Cannot cast NaN value to Integer dtype"
        with pytest.raises(ValueError, match=msg):
            IntegerArray._from_sequence(values, dtype=to_dtype)
        with pytest.raises(ValueError, match=msg):
            pd.array(values, dtype=result_dtype())
        return

    result = IntegerArray._from_sequence(values, dtype=to_dtype)
    assert result.dtype == result_dtype()
    expected = pd.array(values, dtype=result_dtype())
    tm.assert_extension_array_equal(result, expected)

