
def test_constructor_valid_string_view(chunked):
    # requires pyarrow>=18 for casting string_view to string
    pa = pytest.importorskip("pyarrow", minversion="18")

    arr = pa.array(["1", "2", "3"], pa.string_view())
    if chunked:
        arr = pa.chunked_array(arr)

    arr = ArrowStringArray(arr)
    # dictionary type get converted to dense large string array
    assert pa.types.is_large_string(arr._pa_array.type)

