
def _contains_nan(
    a: Array,
    nan_policy: Literal["propagate", "raise", "omit"] = "propagate",
    *,
    xp_omit_okay: bool = False,
    xp: ModuleType | None = None,
) -> Array | bool:
    # Regarding `xp_omit_okay`: Temporarily, while `_axis_nan_policy` does not
    # handle non-NumPy arrays, most functions that call `_contains_nan` want
    # it to raise an error if `nan_policy='omit'` and `xp` is not `np`.
    # Some functions support `nan_policy='omit'` natively, so setting this to
    # `True` prevents the error from being raised.
    policies = {"propagate", "raise", "omit"}
    if nan_policy not in policies:
        msg = f"nan_policy must be one of {policies}."
        raise ValueError(msg)

    if xp_size(a) == 0:
        return False

    if xp is None:
        xp = array_namespace(a)

    if xp.isdtype(a.dtype, "real floating"):
        # Faster and less memory-intensive than xp.any(xp.isnan(a)), and unlike other
        # reductions, `max`/`min` won't return NaN unless there is a NaN in the data.
        contains_nan = xp.isnan(xp.max(a))
    elif xp.isdtype(a.dtype, "complex floating"):
        # Typically `real` and `imag` produce views; otherwise, `xp.any(xp.isnan(a))`
        # would be more efficient.
        contains_nan = xp.isnan(xp.max(xp.real(a))) | xp.isnan(xp.max(xp.imag(a)))
    elif is_numpy(xp) and np.issubdtype(a.dtype, object):
        contains_nan = False
        for el in a.ravel():
            # isnan doesn't work on non-numeric elements
            if np.issubdtype(type(el), np.number) and np.isnan(el):
                contains_nan = True
                break
    else:
        # Only `object` and `inexact` arrays can have NaNs
        return False

    # The implicit call to bool(contains_nan) must happen after testing
    # nan_policy to prevent lazy and device-bound xps from raising in the
    # default policy='propagate' case.
    if nan_policy == 'raise':
        if is_lazy_array(a):
            msg = "nan_policy='raise' is not supported for lazy arrays."
            raise TypeError(msg)
        if contains_nan:
            msg = "The input contains nan values"
            raise ValueError(msg)
    elif nan_policy == 'omit' and not xp_omit_okay and not is_numpy(xp):
        if is_lazy_array(a):
            msg = "nan_policy='omit' is not supported for lazy arrays."
            raise TypeError(msg)

    return contains_nan

