
def test_index_str_accessor_non_string_values_raises(
    values, inferred_type, index_or_series
):
    obj = index_or_series(values)
    if index_or_series is Index:
        assert obj.inferred_type == inferred_type

    msg = "Can only use .str accessor with string values"
    with pytest.raises(AttributeError, match=msg):
        obj.str

