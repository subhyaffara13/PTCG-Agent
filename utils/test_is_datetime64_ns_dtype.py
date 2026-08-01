
def test_is_datetime64_ns_dtype():
    assert not com.is_datetime64_ns_dtype(int)
    assert not com.is_datetime64_ns_dtype(str)
    assert not com.is_datetime64_ns_dtype(np.datetime64)
    assert not com.is_datetime64_ns_dtype(np.array([1, 2]))
    assert not com.is_datetime64_ns_dtype(np.array(["a", "b"]))
    assert not com.is_datetime64_ns_dtype(np.array([], dtype=np.datetime64))

    # This datetime array has the wrong unit (ps instead of ns)
    assert not com.is_datetime64_ns_dtype(np.array([], dtype="datetime64[ps]"))

    assert com.is_datetime64_ns_dtype(DatetimeTZDtype("ns", "US/Eastern"))
    assert com.is_datetime64_ns_dtype(
        pd.DatetimeIndex([1, 2, 3], dtype=np.dtype("datetime64[ns]"))
    )

    # non-nano dt64tz
    assert not com.is_datetime64_ns_dtype(DatetimeTZDtype("us", "US/Eastern"))

