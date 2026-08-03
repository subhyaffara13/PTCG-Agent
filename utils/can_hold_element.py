from typing import Any

def can_hold_element(arr: ArrayLike, element: Any) -> bool:
    """
    Can we do an inplace setitem with this element in an array with this dtype?

    Parameters
    ----------
    arr : np.ndarray or ExtensionArray
    element : Any

    Returns
    -------
    bool
    """
    dtype = arr.dtype
    if not isinstance(dtype, np.dtype) or dtype.kind in "mM":
        if isinstance(dtype, (PeriodDtype, IntervalDtype, DatetimeTZDtype, np.dtype)):
            # np.dtype here catches datetime64ns and timedelta64ns; we assume
            #  in this case that we have DatetimeArray/TimedeltaArray
            arr = cast(
                "PeriodArray | DatetimeArray | TimedeltaArray | IntervalArray", arr
            )
            try:
                arr._validate_setitem_value(element)
                return True
            except (ValueError, TypeError):
                return False

        if dtype == "string":
            try:
                arr._maybe_convert_setitem_value(element)  # type: ignore[union-attr]
                return True
            except (ValueError, TypeError):
                return False

        # This is technically incorrect, but maintains the behavior of
        # ExtensionBlock._can_hold_element
        return True

    try:
        np_can_hold_element(dtype, element)
        return True
    except (TypeError, LossySetitemError):
        return False

