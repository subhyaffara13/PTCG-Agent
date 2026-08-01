
def test_is_not_int64_dtype(dtype):
    msg = "is_int64_dtype is deprecated"
    with tm.assert_produces_warning(DeprecationWarning, match=msg):
        assert not com.is_int64_dtype(dtype)

