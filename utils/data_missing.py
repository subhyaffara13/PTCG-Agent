
def data_missing():
    """Length-2 array with [NA, Valid]"""
    raise NotImplementedError


def data_missing(data):
    """Length-2 array with [NA, Valid]"""
    return type(data)._from_sequence([None, data[0]], dtype=data.dtype)


def data_missing():
    """Length 2 array with [NA, Valid]"""
    return Categorical([np.nan, "A"])


def data_missing(dtype):
    return DatetimeArray._from_sequence(
        np.array(["NaT", "2000-01-01"], dtype="datetime64[ns]"), dtype=dtype
    )


def data_missing():
    """Length 2 array with [NA, Valid]"""
    return IntervalArray.from_tuples([None, (0, 1)])


def data_missing(dtype):
    if dtype.kind == "f":
        return pd.array([pd.NA, 0.1], dtype=dtype)
    elif dtype.kind == "b":
        return pd.array([np.nan, True], dtype=dtype)
    return pd.array([pd.NA, 1], dtype=dtype)


def data_missing(allow_in_pandas, dtype):
    if dtype.numpy_dtype == "object":
        return NumpyExtensionArray(np.array([np.nan, (1,)], dtype=object))
    return NumpyExtensionArray(np.array([np.nan, 1.0]))


def data_missing(dtype):
    return PeriodArray([iNaT, 2017], dtype=dtype)


def data_missing(request):
    """Length 2 array with [NA, Valid]"""
    return SparseArray([np.nan, 1], fill_value=request.param)


def data_missing(dtype, chunked):
    """Length 2 array with [NA, Valid]"""
    arr = dtype.construct_array_type()._from_sequence([pd.NA, "A"], dtype=dtype)
    return maybe_split_array(arr, chunked)


def data_missing():
    return DecimalArray([decimal.Decimal("NaN"), decimal.Decimal(1)])


def data_missing():
    """Length 2 array with [NA, Valid]"""
    return JSONArray([{}, {"a": 10}])


def data_missing(dtype):
    """
    Fixture returning array with missing data according to parametrized float
    'dtype'.
    """
    return pd.array([pd.NA, 0.1], dtype=dtype)


def data_missing(dtype):
    """
    Fixture returning array with exactly one NaN and one valid integer,
    according to parametrized integer 'dtype'.

    Used to test dtype conversion with and without missing values.
    """
    return pd.array([pd.NA, 1], dtype=dtype)

