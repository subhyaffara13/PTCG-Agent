
def _sequence_to_dt64(
    data: ArrayLike,
    *,
    copy: bool = False,
    tz: tzinfo | None = None,
    dayfirst: bool = False,
    yearfirst: bool = False,
    ambiguous: TimeAmbiguous = "raise",
    out_unit: str | None = None,
) -> tuple[np.ndarray, tzinfo | None]:
    """
    Parameters
    ----------
    data : np.ndarray or ExtensionArray
        dtl.ensure_arraylike_for_datetimelike has already been called.
    copy : bool, default False
    tz : tzinfo or None, default None
    dayfirst : bool, default False
    yearfirst : bool, default False
    ambiguous : str, bool, or arraylike, default 'raise'
        See pandas._libs.tslibs.tzconversion.tz_localize_to_utc.
    out_unit : str or None, default None
        Desired output resolution.

    Returns
    -------
    result : numpy.ndarray
        The sequence converted to a numpy array with dtype ``datetime64[unit]``.
        Where `unit` is "ns" unless specified otherwise by `out_unit`.
    tz : tzinfo or None
        Either the user-provided tzinfo or one inferred from the data.

    Raises
    ------
    TypeError : PeriodDType data is passed
    """

    # By this point we are assured to have either a numpy array or Index
    data, copy = maybe_convert_dtype(data, copy, tz=tz)
    data_dtype = getattr(data, "dtype", None)

    out_dtype = DT64NS_DTYPE
    if out_unit is not None:
        out_dtype = np.dtype(f"M8[{out_unit}]")

    if data_dtype == object or is_string_dtype(data_dtype):
        # TODO: We do not have tests specific to string-dtypes,
        #  also complex or categorical or other extension
        data = cast(np.ndarray, data)
        copy = False
        if lib.infer_dtype(data, skipna=False) == "integer":
            # Much more performant than going through array_to_datetime
            data = data.astype(np.int64)
        elif tz is not None and ambiguous == "raise":
            obj_data = np.asarray(data, dtype=object)
            result = tslib.array_to_datetime_with_tz(
                obj_data,
                tz=tz,
                dayfirst=dayfirst,
                yearfirst=yearfirst,
                creso=abbrev_to_npy_unit(out_unit),
            )
            return result, tz
        else:
            converted, inferred_tz = objects_to_datetime64(
                data,
                dayfirst=dayfirst,
                yearfirst=yearfirst,
                allow_object=False,
                out_unit=out_unit,
            )
            copy = False
            if tz and inferred_tz:
                #  two timezones: convert to intended from base UTC repr
                # GH#42505 by convention, these are _already_ UTC
                result = converted

            elif inferred_tz:
                tz = inferred_tz
                result = converted

            else:
                result, _ = _construct_from_dt64_naive(
                    converted, tz=tz, copy=copy, ambiguous=ambiguous
                )
            return result, tz

        data_dtype = data.dtype

    # `data` may have originally been a Categorical[datetime64[ns, tz]],
    # so we need to handle these types.
    if isinstance(data_dtype, DatetimeTZDtype):
        # DatetimeArray -> ndarray
        data = cast(DatetimeArray, data)
        tz = _maybe_infer_tz(tz, data.tz)
        result = data._ndarray

    elif lib.is_np_dtype(data_dtype, "M"):
        # tz-naive DatetimeArray or ndarray[datetime64]
        if isinstance(data, DatetimeArray):
            data = data._ndarray

        data = cast(np.ndarray, data)
        result, copy = _construct_from_dt64_naive(
            data, tz=tz, copy=copy, ambiguous=ambiguous
        )

    else:
        # must be integer dtype otherwise
        # assume this data are epoch timestamps
        if data.dtype != INT64_DTYPE:
            data = data.astype(np.int64, copy=False)
            copy = False
        data = cast(np.ndarray, data)
        result = data.view(out_dtype)

    if copy:
        result = result.copy()

    assert isinstance(result, np.ndarray), type(result)
    assert result.dtype.kind == "M"
    assert result.dtype != "M8"
    assert is_supported_dtype(result.dtype)
    return result, tz

