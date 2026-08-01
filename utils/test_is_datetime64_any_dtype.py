
def test_is_datetime64_any_dtype():
    assert not com.is_datetime64_any_dtype(int)
    assert not com.is_datetime64_any_dtype(str)
    assert not com.is_datetime64_any_dtype(np.array([1, 2]))
    assert not com.is_datetime64_any_dtype(np.array(["a", "b"]))

    assert com.is_datetime64_any_dtype(np.datetime64)
    assert com.is_datetime64_any_dtype(np.array([], dtype=np.datetime64))
    assert com.is_datetime64_any_dtype(DatetimeTZDtype("ns", "US/Eastern"))
    assert com.is_datetime64_any_dtype(
        pd.DatetimeIndex([1, 2, 3], dtype="datetime64[ns]")
    )


def test_is_datetime64_any_dtype(data):
    pa_type = data.dtype.pyarrow_dtype
    if pa.types.is_timestamp(pa_type) or pa.types.is_date(pa_type):
        assert is_datetime64_any_dtype(data)
    else:
        assert not is_datetime64_any_dtype(data)

