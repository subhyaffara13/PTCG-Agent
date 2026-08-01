
def find_valid_index(how: str, is_valid: npt.NDArray[np.bool_]) -> int | None:
    """
    Retrieves the positional index of the first valid value.

    Parameters
    ----------
    how : {'first', 'last'}
        Use this parameter to change between the first or last valid index.
    is_valid: np.ndarray
        Mask to find na_values.

    Returns
    -------
    int or None
    """
    assert how in ["first", "last"]

    if len(is_valid) == 0:  # early stop
        return None

    if is_valid.ndim == 2:
        # reduce axis 1
        is_valid = is_valid.any(axis=1)  # type: ignore[assignment]

    if how == "first":
        idxpos = is_valid[::].argmax()

    elif how == "last":
        idxpos = len(is_valid) - 1 - is_valid[::-1].argmax()

    chk_notna = is_valid[idxpos]

    if not chk_notna:
        return None
    # Incompatible return value type (got "signedinteger[Any]",
    # expected "Optional[int]")
    return idxpos  # type: ignore[return-value]

