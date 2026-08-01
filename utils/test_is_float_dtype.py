
def test_is_float_dtype():
    assert not com.is_float_dtype(str)
    assert not com.is_float_dtype(int)
    assert not com.is_float_dtype(pd.Series([1, 2]))
    assert not com.is_float_dtype(np.array(["a", "b"]))

    assert com.is_float_dtype(float)
    assert com.is_float_dtype(pd.Index([1, 2.0]))


def test_is_float_dtype(data):
    pa_type = data.dtype.pyarrow_dtype
    if pa.types.is_floating(pa_type):
        assert is_float_dtype(data)
    else:
        assert not is_float_dtype(data)

