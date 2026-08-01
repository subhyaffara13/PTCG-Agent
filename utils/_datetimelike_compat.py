
def _datetimelike_compat(func: F) -> F:
    """
    Wrapper to handle datetime64 and timedelta64 dtypes.
    """

    @wraps(func)
    def new_func(
        values,
        limit: int | None = None,
        limit_area: Literal["inside", "outside"] | None = None,
        mask=None,
    ):
        if needs_i8_conversion(values.dtype):
            if mask is None:
                # This needs to occur before casting to int64
                mask = isna(values)

            result, mask = func(
                values.view("i8"), limit=limit, limit_area=limit_area, mask=mask
            )
            return result.view(values.dtype), mask

        return func(values, limit=limit, limit_area=limit_area, mask=mask)

    return cast(F, new_func)


def _datetimelike_compat(func: F) -> F:
    """
    If we have datetime64 or timedelta64 values, ensure we have a correct
    mask before calling the wrapped function, then cast back afterwards.
    """

    @functools.wraps(func)
    def new_func(
        values: np.ndarray,
        *,
        axis: AxisInt | None = None,
        skipna: bool = True,
        mask: npt.NDArray[np.bool_] | None = None,
        **kwargs,
    ):
        orig_values = values

        datetimelike = values.dtype.kind in "mM"
        if datetimelike and mask is None:
            mask = isna(values)

        result = func(values, axis=axis, skipna=skipna, mask=mask, **kwargs)

        if datetimelike:
            result = _wrap_results(result, orig_values.dtype, fill_value=iNaT)
            if not skipna:
                assert mask is not None  # checked above
                result = _mask_datetimelike_result(result, axis, mask, orig_values)

        return result

    return cast(F, new_func)

