
def tz_to_dtype(tz: tzinfo, unit: TimeUnit = ...) -> DatetimeTZDtype: ...


def tz_to_dtype(tz: None, unit: TimeUnit = ...) -> np.dtype[np.datetime64]: ...


def tz_to_dtype(
    tz: tzinfo | None, unit: TimeUnit = "ns"
) -> np.dtype[np.datetime64] | DatetimeTZDtype:
    """
    Return a datetime64[ns] dtype appropriate for the given timezone.

    Parameters
    ----------
    tz : tzinfo or None
    unit : str, default "ns"

    Returns
    -------
    np.dtype or Datetime64TZDType
    """
    if tz is None:
        return np.dtype(f"M8[{unit}]")
    else:
        return DatetimeTZDtype(tz=tz, unit=unit)

