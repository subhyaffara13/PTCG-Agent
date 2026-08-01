
def find_result_type(left_dtype: DtypeObj, right: Any) -> DtypeObj:
    """
    Find the type/dtype for the result of an operation between objects.

    This is similar to find_common_type, but looks at the right object instead
    of just its dtype. This can be useful in particular when the right
    object does not have a `dtype`.

    Parameters
    ----------
    left_dtype : np.dtype or ExtensionDtype
    right : Any

    Returns
    -------
    np.dtype or ExtensionDtype

    See also
    --------
    find_common_type
    numpy.result_type
    """
    new_dtype: DtypeObj

    if (
        isinstance(left_dtype, np.dtype)
        and left_dtype.kind in "iuc"
        and (lib.is_integer(right) or lib.is_float(right))
    ):
        # e.g. with int8 dtype and right=512, we want to end up with
        # np.int16, whereas infer_dtype_from(512) gives np.int64,
        #  which will make us upcast too far.
        if lib.is_float(right) and right.is_integer() and left_dtype.kind != "f":
            right = int(right)
        # After NEP 50, numpy won't inspect Python scalars
        # TODO: do we need to recreate numpy's inspection logic for floats too
        # (this breaks some tests)
        if isinstance(right, int) and not isinstance(right, np.integer):
            # This gives an unsigned type by default
            # (if our number is positive)

            # If our left dtype is signed, we might not want this since
            # this might give us 1 dtype too big
            # We should check if the corresponding int dtype (e.g. int64 for uint64)
            # can hold the number
            right_dtype = np.min_scalar_type(right)
            if right == 0:
                # Special case 0
                right = left_dtype
            elif (
                not np.issubdtype(left_dtype, np.unsignedinteger)
                and 0 < right <= np.iinfo(right_dtype).max
            ):
                # If left dtype isn't unsigned, check if it fits in the signed dtype
                right = np.dtype(f"i{right_dtype.itemsize}")
            else:
                right = right_dtype

        new_dtype = np.result_type(left_dtype, right)

    elif is_valid_na_for_dtype(right, left_dtype):
        # e.g. IntervalDtype[int] and None/np.nan
        new_dtype = ensure_dtype_can_hold_na(left_dtype)

    else:
        dtype, _ = infer_dtype_from(right)
        new_dtype = find_common_type([left_dtype, dtype])

    return new_dtype

