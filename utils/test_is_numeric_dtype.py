
def test_is_numeric_dtype():
    assert not com.is_numeric_dtype(str)
    assert not com.is_numeric_dtype(np.datetime64)
    assert not com.is_numeric_dtype(np.timedelta64)
    assert not com.is_numeric_dtype(np.array(["a", "b"]))
    assert not com.is_numeric_dtype(np.array([], dtype="m8[ns]"))

    assert com.is_numeric_dtype(int)
    assert com.is_numeric_dtype(float)
    assert com.is_numeric_dtype(np.uint64)
    assert com.is_numeric_dtype(pd.Series([1, 2]))
    assert com.is_numeric_dtype(pd.Index([1, 2.0]))

    class MyNumericDType(ExtensionDtype):
        @property
        def type(self):
            return str

        @property
        def name(self):
            raise NotImplementedError

        def construct_array_type(self):
            raise NotImplementedError

        def _is_numeric(self) -> bool:
            return True

    assert com.is_numeric_dtype(MyNumericDType())


def test_is_numeric_dtype(data):
    # GH 50563
    pa_type = data.dtype.pyarrow_dtype
    if (
        pa.types.is_floating(pa_type)
        or pa.types.is_integer(pa_type)
        or pa.types.is_decimal(pa_type)
    ):
        assert is_numeric_dtype(data)
    else:
        assert not is_numeric_dtype(data)

