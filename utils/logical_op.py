
def logical_op(left: ArrayLike, right: Any, op) -> ArrayLike:
    """
    Evaluate a logical operation `|`, `&`, or `^`.

    Parameters
    ----------
    left : np.ndarray or ExtensionArray
    right : object
        Cannot be a DataFrame, Series, or Index.
    op : {operator.and_, operator.or_, operator.xor}
        Or one of the reversed variants from roperator.

    Returns
    -------
    ndarray or ExtensionArray
    """

    def fill_bool(x, left=None):
        # if `left` is specifically not-boolean, we do not cast to bool
        if x.dtype.kind in "cfO":
            # dtypes that can hold NA
            mask = isna(x)
            if mask.any():
                x = x.astype(object)
                x[mask] = False

        if left is None or left.dtype.kind == "b":
            x = x.astype(bool)
        return x

    right = lib.item_from_zerodim(right)
    if is_list_like(right) and not hasattr(right, "dtype"):
        # e.g. list, tuple
        raise TypeError(
            # GH#52264
            "Logical ops (and, or, xor) between Pandas objects and dtype-less "
            "sequences (e.g. list, tuple) are no longer supported. "
            "Wrap the object in a Series, Index, or np.array "
            "before operating instead.",
        )

    # NB: We assume extract_array has already been called on left and right
    lvalues = ensure_wrapped_if_datetimelike(left)
    rvalues = right

    if should_extension_dispatch(lvalues, rvalues):
        # Call the method on lvalues
        res_values = op(lvalues, rvalues)

    else:
        if isinstance(rvalues, np.ndarray):
            is_other_int_dtype = rvalues.dtype.kind in "iu"
            if not is_other_int_dtype:
                rvalues = fill_bool(rvalues, lvalues)

        else:
            # i.e. scalar
            is_other_int_dtype = lib.is_integer(rvalues)

        res_values = na_logical_op(lvalues, rvalues, op)

        # For int vs int `^`, `|`, `&` are bitwise operators and return
        #   integer dtypes.  Otherwise these are boolean ops
        if not (left.dtype.kind in "iu" and is_other_int_dtype):
            res_values = fill_bool(res_values)

    return res_values

