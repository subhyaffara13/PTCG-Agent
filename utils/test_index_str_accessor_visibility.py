
def test_index_str_accessor_visibility(values, inferred_type, index_or_series):
    obj = index_or_series(values)
    if index_or_series is Index:
        assert obj.inferred_type == inferred_type

    assert isinstance(obj.str, StringMethods)

