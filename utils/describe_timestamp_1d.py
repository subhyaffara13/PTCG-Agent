
def describe_timestamp_1d(data: Series, percentiles: Sequence[float]) -> Series:
    """Describe series containing datetime64 dtype.

    Parameters
    ----------
    data : Series
        Series to be described.
    percentiles : list-like of numbers
        The percentiles to include in the output.
    """
    # GH-30164
    from pandas import Series

    formatted_percentiles = format_percentiles(percentiles)

    stat_index = ["count", "mean", "min", *formatted_percentiles, "max"]
    d = [
        data.count(),
        data.mean(),
        data.min(),
        *data.quantile(percentiles).tolist(),
        data.max(),
    ]
    return Series(d, index=stat_index, name=data.name)

