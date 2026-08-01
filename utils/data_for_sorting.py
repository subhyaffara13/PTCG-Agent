
def data_for_sorting():
    """
    Length-3 array with a known sort order.

    This should be three items [B, C, A] with
    A < B < C

    For boolean dtypes (for which there are only 2 values available),
    set B=C=True
    """
    raise NotImplementedError


def data_for_sorting(data_for_grouping):
    """
    Length-3 array with a known sort order.

    This should be three items [B, C, A] with
    A < B < C
    """
    return type(data_for_grouping)._from_sequence(
        [data_for_grouping[0], data_for_grouping[7], data_for_grouping[4]],
        dtype=data_for_grouping.dtype,
    )


def data_for_sorting():
    return Categorical(["A", "B", "C"], categories=["C", "A", "B"], ordered=True)


def data_for_sorting(dtype):
    a = pd.Timestamp("2000-01-01")
    b = pd.Timestamp("2000-01-02")
    c = pd.Timestamp("2000-01-03")
    return DatetimeArray._from_sequence(
        np.array([b, c, a], dtype="datetime64[ns]"), dtype=dtype
    )


def data_for_sorting():
    return IntervalArray.from_tuples([(1, 2), (2, 3), (0, 1)])


def data_for_sorting(dtype):
    if dtype.kind == "f":
        return pd.array([0.1, 0.2, 0.0], dtype=dtype)
    elif dtype.kind == "b":
        return pd.array([True, True, False], dtype=dtype)
    return pd.array([1, 2, 0], dtype=dtype)


def data_for_sorting(allow_in_pandas, dtype):
    """Length-3 array with a known sort order.

    This should be three items [B, C, A] with
    A < B < C
    """
    if dtype.numpy_dtype == "object":
        # Use an empty tuple for first element, then remove,
        # to disable np.array's shape inference.
        return NumpyExtensionArray(np.array([(), (2,), (3,), (1,)], dtype=object)[1:])
    return NumpyExtensionArray(np.array([1, 2, 0]))


def data_for_sorting(dtype):
    return PeriodArray([2018, 2019, 2017], dtype=dtype)


def data_for_sorting(request):
    return SparseArray([2, 3, 1], fill_value=request.param)


def data_for_sorting(dtype, chunked):
    arr = dtype.construct_array_type()._from_sequence(["B", "C", "A"], dtype=dtype)
    return maybe_split_array(arr, chunked)


def data_for_sorting():
    return DecimalArray(
        [decimal.Decimal("1"), decimal.Decimal("2"), decimal.Decimal("0")]
    )


def data_for_sorting():
    return JSONArray([{"b": 1}, {"c": 4}, {"a": 2, "c": 3}])

