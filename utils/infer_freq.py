
def infer_freq(
    index: DatetimeIndex | TimedeltaIndex | Series | DatetimeLikeArrayMixin,
) -> str | None:
    """
    Infer the most likely frequency given the input index.

    This method attempts to deduce the most probable frequency (e.g., 'D' for daily,
    'H' for hourly) from a sequence of datetime-like objects. It is particularly useful
    when the frequency of a time series is not explicitly set or known but can be
    inferred from its values.

    Parameters
    ----------
    index : DatetimeIndex, TimedeltaIndex, Series or array-like
      If passed a Series will use the values of the series (NOT THE INDEX).

    Returns
    -------
    str or None
        None if no discernible frequency.

    Raises
    ------
    TypeError
        If the index is not datetime-like.
    ValueError
        If there are fewer than three values.

    See Also
    --------
    date_range : Return a fixed frequency DatetimeIndex.
    timedelta_range : Return a fixed frequency TimedeltaIndex with day as the default.
    period_range : Return a fixed frequency PeriodIndex.
    DatetimeIndex.freq : Return the frequency object if it is set, otherwise None.

    Examples
    --------
    >>> idx = pd.date_range(start="2020/12/01", end="2020/12/30", periods=30)
    >>> pd.infer_freq(idx)
    'D'
    """
    from pandas.core.api import DatetimeIndex

    if isinstance(index, ABCSeries):
        values = index._values

        if isinstance(index.dtype, ArrowDtype):
            import pyarrow as pa

            if pa.types.is_timestamp(values.dtype.pyarrow_dtype):
                # GH#58403
                values = values._to_datetimearray()

        if not (
            lib.is_np_dtype(values.dtype, "mM")
            or isinstance(values.dtype, DatetimeTZDtype)
            or values.dtype == object
        ):
            raise TypeError(
                "cannot infer freq from a non-convertible dtype "
                f"on a Series of {index.dtype}"
            )
        index = values

    inferer: _FrequencyInferer

    if not hasattr(index, "dtype"):
        pass
    elif isinstance(index.dtype, PeriodDtype):
        raise TypeError(
            "PeriodIndex given. Check the `freq` attribute instead of using infer_freq."
        )
    elif lib.is_np_dtype(index.dtype, "m"):
        # Allow TimedeltaIndex and TimedeltaArray
        inferer = _TimedeltaFrequencyInferer(index)
        return inferer.get_freq()

    elif is_numeric_dtype(index.dtype):
        raise TypeError(
            f"cannot infer freq from a non-convertible index of dtype {index.dtype}"
        )

    if not isinstance(index, DatetimeIndex):
        index = DatetimeIndex(index, copy=False)

    inferer = _FrequencyInferer(index)
    return inferer.get_freq()

