
def has_level_label(label_flags: npt.NDArray[np.intp], vmin: float) -> bool:
    """
    Returns true if the ``label_flags`` indicate there is at least one label
    for this level.

    if the minimum view limit is not an exact integer, then the first tick
    label won't be shown, so we must adjust for that.
    """
    if label_flags.size == 0 or (
        label_flags.size == 1 and label_flags[0] == 0 and vmin % 1 > 0.0
    ):
        return False
    else:
        return True

