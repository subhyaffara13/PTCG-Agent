
def test_roundtrip_randsize():
    for arr in basic_arrays + record_arrays:
        if arr.dtype != object:
            arr2 = roundtrip_randsize(arr)
            assert_array_equal(arr, arr2)

