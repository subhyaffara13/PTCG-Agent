
def _check_patches_all_filled(axes: Axes | Sequence[Axes], filled: bool = True) -> None:
    """
    Check for each artist whether it is filled or not

    Parameters
    ----------
    axes : matplotlib Axes object, or its list-like
    filled : bool
        expected filling
    """

    axes = _flatten_visible(axes)
    for ax in axes:
        for patch in ax.patches:
            assert patch.fill == filled

