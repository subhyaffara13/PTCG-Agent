
def _validate_tz_from_dtype(
    dtype, tz: tzinfo | None, explicit_tz_none: bool = False
) -> tzinfo | None:
    """
    If the given dtype is a DatetimeTZDtype, extract the implied
    tzinfo object from it and check that it does not conflict with the given
    tz.

    Parameters
    ----------
    dtype : dtype, str
    tz : None, tzinfo
    explicit_tz_none : bool, default False
        Whether tz=None was passed explicitly, as opposed to lib.no_default.

    Returns
    -------
    tz : consensus tzinfo

    Raises
    ------
    ValueError : on tzinfo mismatch
    """
    if dtype is not None:
        if isinstance(dtype, str):
            try:
                dtype = DatetimeTZDtype.construct_from_string(dtype)
            except TypeError:
                # Things like `datetime64[ns]`, which is OK for the
                # constructors, but also nonsense, which should be validated
                # but not by us. We *do* allow non-existent tz errors to
                # go through
                pass
        dtz = getattr(dtype, "tz", None)
        if dtz is not None:
            if tz is not None and not timezones.tz_compare(tz, dtz):
                raise ValueError("cannot supply both a tz and a dtype with a tz")
            if explicit_tz_none:
                raise ValueError("Cannot pass both a timezone-aware dtype and tz=None")
            tz = dtz

        if tz is not None and lib.is_np_dtype(dtype, "M"):
            # We also need to check for the case where the user passed a
            #  tz-naive dtype (i.e. datetime64[ns])
            if tz is not None and not timezones.tz_compare(tz, dtz):
                raise ValueError(
                    "cannot supply both a tz and a "
                    "timezone-naive dtype (i.e. datetime64[ns])"
                )

    return tz

