
def test_to_integer_array_none_is_nan(a, b, using_nan_is_na):
    if using_nan_is_na:
        result = pd.array(a, dtype="Int64")
        expected = pd.array(b, dtype="Int64")
        tm.assert_extension_array_equal(result, expected)
    else:
        msg = "Cannot cast NaN value to Integer dtype"
        with pytest.raises(ValueError, match=msg):
            pd.array(b, dtype="Int64")

