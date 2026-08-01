
def concat_compat(
    to_concat: Sequence[ArrayLike], axis: AxisInt = 0, ea_compat_axis: bool = False
) -> ArrayLike:
    """
    provide concatenation of an array of arrays each of which is a single
    'normalized' dtypes (in that for example, if it's object, then it is a
    non-datetimelike and provide a combined dtype for the resulting array that
    preserves the overall dtype if possible)

    Parameters
    ----------
    to_concat : sequence of arrays
    axis : axis to provide concatenation
    ea_compat_axis : bool, default False
        For ExtensionArray compat, behave as if axis == 1 when determining
        whether to drop empty arrays.

    Returns
    -------
    a single array, preserving the combined dtypes
    """
    if len(to_concat) and lib.dtypes_all_equal([obj.dtype for obj in to_concat]):
        # fastpath!
        obj = to_concat[0]
        if isinstance(obj, np.ndarray):
            to_concat_arrs = cast("Sequence[np.ndarray]", to_concat)
            return np.concatenate(to_concat_arrs, axis=axis)

        to_concat_eas = cast("Sequence[ExtensionArray]", to_concat)
        if ea_compat_axis:
            # We have 1D objects, that don't support axis keyword
            return obj._concat_same_type(to_concat_eas)
        elif axis == 0:
            return obj._concat_same_type(to_concat_eas)
        else:
            # e.g. DatetimeArray
            # NB: We are assuming here that ensure_wrapped_if_arraylike has
            #  been called where relevant.
            return obj._concat_same_type(
                # error: Unexpected keyword argument "axis" for "_concat_same_type"
                # of "ExtensionArray"
                to_concat_eas,
                axis=axis,  # type: ignore[call-arg]
            )

    # If all arrays are empty, there's nothing to convert, just short-cut to
    # the concatenation, #3121.
    #
    # Creating an empty array directly is tempting, but the winnings would be
    # marginal given that it would still require shape & dtype calculation and
    # np.concatenate which has them both implemented is compiled.
    non_empties = [x for x in to_concat if _is_nonempty(x, axis)]

    any_ea, kinds, target_dtype = _get_result_dtype(to_concat, non_empties)

    if target_dtype is not None:
        to_concat = [astype_array(arr, target_dtype, copy=False) for arr in to_concat]

    if not isinstance(to_concat[0], np.ndarray):
        # i.e. isinstance(to_concat[0], ExtensionArray)
        to_concat_eas = cast("Sequence[ExtensionArray]", to_concat)
        cls = type(to_concat[0])
        # GH#53640: eg. for datetime array, axis=1 but 0 is default
        # However, class method `_concat_same_type()` for some classes
        # may not support the `axis` keyword
        if ea_compat_axis or axis == 0:
            return cls._concat_same_type(to_concat_eas)
        else:
            return cls._concat_same_type(
                to_concat_eas,
                axis=axis,  # type: ignore[call-arg]
            )
    else:
        to_concat_arrs = cast("Sequence[np.ndarray]", to_concat)
        result = np.concatenate(to_concat_arrs, axis=axis)

        if not any_ea and "b" in kinds and result.dtype.kind in "iuf":
            # GH#39817 cast to object instead of casting bools to numeric
            result = result.astype(object, copy=False)
    return result

