
def data_for_twos(dtype):
    """
    Length-10 array in which all the elements are two.

    Call pytest.skip in your fixture if the dtype does not support divmod.
    """
    if not (dtype._is_numeric or dtype.kind == "m"):
        # Object-dtypes may want to allow this, but for the most part
        #  only numeric and timedelta-like dtypes will need to implement this.
        pytest.skip(f"{dtype} is not a numeric dtype")

    raise NotImplementedError


def data_for_twos(data):
    """Length-100 array in which all the elements are two."""
    pa_dtype = data.dtype.pyarrow_dtype
    if (
        pa.types.is_integer(pa_dtype)
        or pa.types.is_floating(pa_dtype)
        or pa.types.is_decimal(pa_dtype)
        or pa.types.is_duration(pa_dtype)
    ):
        return pd.array([2] * 10, dtype=data.dtype)
    # tests will be xfailed where 2 is not a valid scalar for pa_dtype
    return data


def data_for_twos():
    pytest.skip("Interval is not a numeric dtype")


def data_for_twos(dtype):
    if dtype.kind == "b":
        return pd.array(np.ones(10), dtype=dtype)
    return pd.array(np.ones(10) * 2, dtype=dtype)


def data_for_twos(dtype):
    if dtype.kind == "O":
        pytest.skip(f"{dtype} is not a numeric dtype")
    arr = np.ones(10) * 2
    return NumpyExtensionArray._from_sequence(arr, dtype=dtype)


def data_for_twos():
    return SparseArray(np.ones(10) * 2)


def data_for_twos():
    return DecimalArray([decimal.Decimal(2) for _ in range(10)])

