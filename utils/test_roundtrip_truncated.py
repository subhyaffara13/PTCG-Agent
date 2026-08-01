
def test_roundtrip_truncated():
    for arr in basic_arrays:
        if arr.dtype != object:
            assert_raises(ValueError, roundtrip_truncated, arr)

