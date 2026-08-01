
def validate_clip_with_axis(axis: ndarray, args, kwargs) -> None: ...


def validate_clip_with_axis(axis: AxisNoneT, args, kwargs) -> AxisNoneT: ...


def validate_clip_with_axis(
    axis: ndarray | AxisNoneT, args, kwargs
) -> AxisNoneT | None:
    """
    If 'NDFrame.clip' is called via the numpy library, the third parameter in
    its signature is 'out', which can takes an ndarray, so check if the 'axis'
    parameter is an instance of ndarray, since 'axis' itself should either be
    an integer or None
    """
    if isinstance(axis, ndarray):
        args = (axis, *args)
        # error: Incompatible types in assignment (expression has type "None",
        # variable has type "Union[ndarray[Any, Any], str, int]")
        axis = None  # type: ignore[assignment]

    validate_clip(args, kwargs)
    # error: Incompatible return value type (got "Union[ndarray[Any, Any],
    # str, int]", expected "Union[str, int, None]")
    return axis  # type: ignore[return-value]

