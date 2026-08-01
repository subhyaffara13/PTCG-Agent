
def test_is_timedelta64_ns_dtype():
    assert not com.is_timedelta64_ns_dtype(np.dtype("m8[ps]"))
    assert not com.is_timedelta64_ns_dtype(np.array([1, 2], dtype="m8"))

    assert com.is_timedelta64_ns_dtype(np.dtype("m8[ns]"))
    assert com.is_timedelta64_ns_dtype(np.array([1, 2], dtype="m8[ns]"))

