
def data_missing_for_sorting():
    """
    Length-3 array with a known sort order.

    This should be three items [B, NA, A] with
    A < B and NA missing.
    """
    raise NotImplementedError


def data_missing_for_sorting(data_for_grouping):
    """
    Length-3 array with a known sort order.

    This should be three items [B, NA, A] with
    A < B and NA missing.
    """
    return type(data_for_grouping)._from_sequence(
        [data_for_grouping[0], data_for_grouping[2], data_for_grouping[4]],
        dtype=data_for_grouping.dtype,
    )


def data_missing_for_sorting():
    return Categorical(["A", None, "B"], categories=["B", "A"], ordered=True)


def data_missing_for_sorting(dtype):
    a = pd.Timestamp("2000-01-01")
    b = pd.Timestamp("2000-01-02")
    return DatetimeArray._from_sequence(
        np.array([b, "NaT", a], dtype="datetime64[ns]"), dtype=dtype
    )


def data_missing_for_sorting():
    return IntervalArray.from_tuples([(1, 2), None, (0, 1)])


def data_missing_for_sorting(dtype):
    if dtype.kind == "f":
        return pd.array([0.1, pd.NA, 0.0], dtype=dtype)
    elif dtype.kind == "b":
        return pd.array([True, np.nan, False], dtype=dtype)
    return pd.array([1, pd.NA, 0], dtype=dtype)


def data_missing_for_sorting(allow_in_pandas, dtype):
    """Length-3 array with a known sort order.

    This should be three items [B, NA, A] with
    A < B and NA missing.
    """
    if dtype.numpy_dtype == "object":
        return NumpyExtensionArray(np.array([(1,), np.nan, (0,)], dtype=object))
    return NumpyExtensionArray(np.array([1, np.nan, 0]))


def data_missing_for_sorting(dtype):
    return PeriodArray([2018, iNaT, 2017], dtype=dtype)


def data_missing_for_sorting(request):
    return SparseArray([2, np.nan, 1], fill_value=request.param)


def data_missing_for_sorting(dtype, chunked):
    arr = dtype.construct_array_type()._from_sequence(["B", pd.NA, "A"], dtype=dtype)
    return maybe_split_array(arr, chunked)


def data_missing_for_sorting():
    return DecimalArray(
        [decimal.Decimal("1"), decimal.Decimal("NaN"), decimal.Decimal("0")]
    )


def data_missing_for_sorting():
    return JSONArray([{"b": 1}, {}, {"a": 4}])

