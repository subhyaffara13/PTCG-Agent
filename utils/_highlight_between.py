
def _highlight_between(
    data: NDFrame,
    props: str,
    left: Scalar | Sequence | np.ndarray | NDFrame | None = None,
    right: Scalar | Sequence | np.ndarray | NDFrame | None = None,
    inclusive: bool | str = True,
) -> np.ndarray:
    """
    Return an array of css props based on condition of data values within given range.
    """
    if np.iterable(left) and not isinstance(left, str):
        left = _validate_apply_axis_arg(left, "left", None, data)

    if np.iterable(right) and not isinstance(right, str):
        right = _validate_apply_axis_arg(right, "right", None, data)

    # get ops with correct boundary attribution
    if inclusive == "both":
        ops = (operator.ge, operator.le)
    elif inclusive == "neither":
        ops = (operator.gt, operator.lt)
    elif inclusive == "left":
        ops = (operator.ge, operator.lt)
    elif inclusive == "right":
        ops = (operator.gt, operator.le)
    else:
        raise ValueError(
            f"'inclusive' values can be 'both', 'left', 'right', or 'neither' "
            f"got {inclusive}"
        )

    g_left = (
        # error: Argument 2 to "ge" has incompatible type "Union[str, float,
        # Period, Timedelta, Interval[Any], datetime64, timedelta64, datetime,
        # Sequence[Any], ndarray[Any, Any], NDFrame]"; expected "Union
        # [SupportsDunderLE, SupportsDunderGE, SupportsDunderGT, SupportsDunderLT]"
        ops[0](data, left)  # type: ignore[arg-type]
        if left is not None
        else np.full(data.shape, True, dtype=bool)
    )
    if isinstance(g_left, (DataFrame, Series)):
        g_left = g_left.where(pd.notna(g_left), False)
    l_right = (
        # error: Argument 2 to "le" has incompatible type "Union[str, float,
        # Period, Timedelta, Interval[Any], datetime64, timedelta64, datetime,
        # Sequence[Any], ndarray[Any, Any], NDFrame]"; expected "Union
        # [SupportsDunderLE, SupportsDunderGE, SupportsDunderGT, SupportsDunderLT]"
        ops[1](data, right)  # type: ignore[arg-type]
        if right is not None
        else np.full(data.shape, True, dtype=bool)
    )
    if isinstance(l_right, (DataFrame, Series)):
        l_right = l_right.where(pd.notna(l_right), False)
    return np.where(g_left & l_right, props, "")

