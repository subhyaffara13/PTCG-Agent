
def mask_missing(arr: ArrayLike, value) -> npt.NDArray[np.bool_]:
    """
    Return a masking array of same size/shape as arr
    with entries equaling value set to True.

    Parameters
    ----------
    arr : ArrayLike
    value : scalar-like
        Caller has ensured `not is_list_like(value)` and that it can be held
        by `arr`.

    Returns
    -------
    np.ndarray[bool]
    """
    dtype, value = infer_dtype_from(value)

    if (
        isinstance(arr.dtype, (BaseMaskedDtype, ArrowDtype))
        and lib.is_float(value)
        and np.isnan(value)
        and not is_nan_na()
    ):
        # TODO: this should be done in an EA method?
        if arr.dtype.kind == "f":
            # GH#55127
            if isinstance(arr.dtype, BaseMaskedDtype):
                # error: "ExtensionArray" has no attribute "_data"  [attr-defined]
                mask = np.isnan(arr._data) & ~arr.isna()  # type: ignore[attr-defined,operator]
                return mask
            else:
                # error: "ExtensionArray" has no attribute "_pa_array"  [attr-defined]
                import pyarrow.compute as pc

                mask = pc.is_nan(arr._pa_array).fill_null(False).to_numpy()  # type: ignore[attr-defined]
                return mask

        elif arr.dtype.kind in "iu":
            # GH#51237
            mask = np.zeros(arr.shape, dtype=bool)
            return mask

    if isna(value):
        return isna(arr)

    # GH 21977
    mask = np.zeros(arr.shape, dtype=bool)
    if (
        is_numeric_dtype(arr.dtype)
        and not is_bool_dtype(arr.dtype)
        and lib.is_bool(value)
    ):
        # e.g. test_replace_ea_float_with_bool, see GH#62048
        pass
    elif (
        is_bool_dtype(arr.dtype) and is_numeric_dtype(dtype) and not lib.is_bool(value)
    ):
        # e.g. test_replace_ea_float_with_bool, see GH#62048
        pass
    elif is_numeric_dtype(arr.dtype) and isinstance(value, str):
        # GH#29553 prevent numpy deprecation warnings
        pass
    elif is_object_dtype(arr.dtype):
        # pre-compute mask to avoid comparison to NA
        # e.g. test_replace_na_in_obj_column
        arr_mask = ~isna(arr)
        mask[arr_mask] = arr[arr_mask] == value
    else:
        new_mask = arr == value

        if not isinstance(new_mask, np.ndarray):
            # usually BooleanArray
            new_mask = new_mask.to_numpy(dtype=bool, na_value=False)
        mask = new_mask

    return mask

