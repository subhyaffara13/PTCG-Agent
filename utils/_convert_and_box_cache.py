
def _convert_and_box_cache(
    arg: DatetimeScalarOrArrayConvertible,
    cache_array: Series,
    name: Hashable | None = None,
) -> Index:
    """
    Convert array of dates with a cache and wrap the result in an Index.

    Parameters
    ----------
    arg : integer, float, string, datetime, list, tuple, 1-d array, Series
    cache_array : Series
        Cache of converted, unique dates
    name : string, default None
        Name for a DatetimeIndex

    Returns
    -------
    result : Index-like of converted dates
    """
    from pandas import Series

    result = Series(arg, dtype=cache_array.index.dtype).map(cache_array)
    return _box_as_indexlike(result._values, utc=False, name=name)

