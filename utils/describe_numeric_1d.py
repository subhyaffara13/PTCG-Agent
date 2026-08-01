
def describe_numeric_1d(series: Series, percentiles: Sequence[float]) -> Series:
    """Describe series containing numerical data.

    Parameters
    ----------
    series : Series
        Series to be described.
    percentiles : list-like of numbers
        The percentiles to include in the output.
    """
    from pandas import Series

    formatted_percentiles = format_percentiles(percentiles)

    if len(percentiles) == 0:
        quantiles = []
    else:
        quantiles = series.quantile(percentiles).tolist()

    stat_index = ["count", "mean", "std", "min", *formatted_percentiles, "max"]
    d = [
        series.count(),
        series.mean(),
        series.std(),
        series.min(),
        *quantiles,
        series.max(),
    ]
    # GH#48340 - always return float on non-complex numeric data
    dtype: DtypeObj | None
    if isinstance(series.dtype, ExtensionDtype):
        if isinstance(series.dtype, ArrowDtype):
            if series.dtype.kind == "m":
                # GH53001: describe timedeltas with object dtype
                dtype = None
            else:
                import pyarrow as pa

                dtype = ArrowDtype(pa.float64())
        else:
            dtype = Float64Dtype()
    elif series.dtype.kind in "iufb":
        # i.e. numeric but exclude complex dtype
        dtype = np.dtype("float")
    else:
        dtype = None
    return Series(d, index=stat_index, name=series.name, dtype=dtype)

