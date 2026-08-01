
def extract_bool_array(mask: ArrayLike) -> npt.NDArray[np.bool_]:
    """
    If we have a SparseArray or BooleanArray, convert it to ndarray[bool].
    """
    if isinstance(mask, ExtensionArray):
        # We could have BooleanArray, Sparse[bool], ...
        #  Except for BooleanArray, this is equivalent to just
        #  np.asarray(mask, dtype=bool)
        mask = mask.to_numpy(dtype=bool, na_value=False)

    mask = np.asarray(mask, dtype=bool)
    return mask

