
def validate_putmask(
    values: ArrayLike | MultiIndex, mask: np.ndarray
) -> tuple[npt.NDArray[np.bool_], bool]:
    """
    Validate mask and check if this putmask operation is a no-op.
    """
    mask = extract_bool_array(mask)
    if mask.shape != values.shape:
        raise ValueError("putmask: mask and data must be the same size")

    noop = not mask.any()
    return mask, noop

