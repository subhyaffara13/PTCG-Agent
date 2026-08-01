
def test_constructor_valid_string_type_value_dictionary(string_type, chunked):
    pa = pytest.importorskip("pyarrow")

    arr = pa.array(["1", "2", "3"], getattr(pa, string_type)()).dictionary_encode()
    if chunked:
        arr = pa.chunked_array(arr)

    arr = ArrowStringArray(arr)
    # dictionary type get converted to dense large string array
    assert pa.types.is_large_string(arr._pa_array.type)

