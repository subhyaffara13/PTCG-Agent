
def asfreq(
    obj: NDFrameT,
    freq,
    method=None,
    how=None,
    normalize: bool = False,
    fill_value=None,
) -> NDFrameT:
    """
    Utility frequency conversion method for Series/DataFrame.

    See :meth:`pandas.NDFrame.asfreq` for full documentation.
    """
    if isinstance(obj.index, PeriodIndex):
        if method is not None:
            raise NotImplementedError("'method' argument is not supported")

        if how is None:
            how = "E"

        if isinstance(freq, BaseOffset):
            if hasattr(freq, "_period_dtype_code"):
                freq = PeriodDtype(freq)._freqstr

        new_obj = obj.copy()
        new_obj.index = obj.index.asfreq(freq, how=how)

    elif len(obj.index) == 0:
        new_obj = obj.copy()

        new_obj.index = _asfreq_compat(obj.index, freq)
    else:
        unit: TimeUnit = "ns"
        if isinstance(obj.index, DatetimeIndex):
            # TODO: should we disallow non-DatetimeIndex?
            unit = obj.index.unit
        dti = date_range(obj.index.min(), obj.index.max(), freq=freq, unit=unit)
        dti.name = obj.index.name
        new_obj = obj.reindex(dti, method=method, fill_value=fill_value)
        if normalize:
            new_obj.index = new_obj.index.normalize()

    return new_obj

