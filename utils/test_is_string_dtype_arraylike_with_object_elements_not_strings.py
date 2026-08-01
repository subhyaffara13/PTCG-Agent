
def test_is_string_dtype_arraylike_with_object_elements_not_strings(data):
    # GH 15585
    assert not com.is_string_dtype(pd.Series(data))

