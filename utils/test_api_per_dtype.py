
def test_api_per_dtype(index_or_series, dtype, any_skipna_inferred_dtype):
    # one instance of parametrized fixture
    box = index_or_series
    inferred_dtype, values = any_skipna_inferred_dtype

    t = box(values, dtype=dtype)  # explicit dtype to avoid casting

    types_passing_constructor = [
        "string",
        "unicode",
        "empty",
        "bytes",
        "mixed",
        "mixed-integer",
    ]
    if inferred_dtype in types_passing_constructor:
        # GH 6106
        assert isinstance(t.str, StringMethods)
    else:
        # GH 9184, GH 23011, GH 23163
        msg = "Can only use .str accessor with string values.*"
        with pytest.raises(AttributeError, match=msg):
            t.str
        assert not hasattr(t, "str")

