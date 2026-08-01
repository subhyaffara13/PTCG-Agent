
def test_is_int64_dtype(dtype):
    msg = "is_int64_dtype is deprecated"
    with tm.assert_produces_warning(DeprecationWarning, match=msg):
        assert com.is_int64_dtype(dtype)

