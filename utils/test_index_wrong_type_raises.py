
def test_index_wrong_type_raises(index_or_series, any_string_dtype, method):
    obj = index_or_series([], dtype=any_string_dtype)
    msg = "expected a string object, not int"

    with pytest.raises(TypeError, match=msg):
        getattr(obj.str, method)(0)

