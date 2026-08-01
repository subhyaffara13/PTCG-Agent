
def _to_datetime_with_unit(arg, unit, name, utc: bool, errors: str) -> Index:
    """
    to_datetime specalized to the case where a 'unit' is passed.
    """
    arg = extract_array(arg, extract_numpy=True)

    # GH#30050 pass an ndarray to tslib.array_to_datetime
    # because it expects an ndarray argument
    if isinstance(arg, IntegerArray):
        arr = arg.astype(f"datetime64[{unit}]")
        tz_parsed = None
    else:
        arg = np.asarray(arg)

        if arg.dtype.kind in "iu":
            # Note we can't do "f" here because that could induce unwanted
            #  rounding GH#14156, GH#20445
            arr = arg.astype(f"datetime64[{unit}]", copy=False)
            dtype = get_supported_dtype(arr.dtype)
            try:
                arr = astype_overflowsafe(arr, dtype, copy=False)
            except OutOfBoundsDatetime:
                if errors == "raise":
                    raise
                arg = arg.astype(object)
                return _to_datetime_with_unit(arg, unit, name, utc, errors)
            tz_parsed = None

        elif arg.dtype.kind == "f":
            with np.errstate(invalid="ignore"):
                int_values = arg.astype(np.int64)
            mask = np.isnan(arg)
            if (mask | (arg == int_values)).all():
                # With all-round-or-NaN entries, we give the requested unit
                #  back like with integers
                result = _to_datetime_with_unit(
                    int_values, unit=unit, name=name, utc=utc, errors=errors
                )
                result._data[mask] = NaT
                return result
            with np.errstate(over="raise"):
                try:
                    arr = cast_from_unit_vectorized(arg, unit=unit)
                except OutOfBoundsDatetime as err:
                    if errors != "raise":
                        return _to_datetime_with_unit(
                            arg.astype(object), unit, name, utc, errors
                        )
                    raise OutOfBoundsDatetime(
                        f"cannot convert input with unit '{unit}'"
                    ) from err

            arr = arr.view("M8[ns]")
            tz_parsed = None
        else:
            arg = arg.astype(object, copy=False)
            arr, tz_parsed = tslib.array_to_datetime(
                arg,
                utc=utc,
                errors=errors,
                unit_for_numerics=unit,
            )

    result = DatetimeIndex(arr, name=name)
    if not isinstance(result, DatetimeIndex):
        return result

    # GH#23758: We may still need to localize the result with tz
    # GH#25546: Apply tz_parsed first (from arg), then tz (from caller)
    # result will be naive but in UTC
    result = result.tz_localize("UTC").tz_convert(tz_parsed)

    if utc:
        if result.tz is None:
            result = result.tz_localize("utc")
        else:
            result = result.tz_convert("utc")
    return result

