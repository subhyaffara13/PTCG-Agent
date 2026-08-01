
def frame_apply(
    obj: DataFrame,
    func: AggFuncType,
    axis: Axis = 0,
    raw: bool = False,
    result_type: str | None = None,
    by_row: Literal[False, "compat"] = "compat",
    engine: str = "python",
    engine_kwargs: dict[str, bool] | None = None,
    args=None,
    kwargs=None,
) -> FrameApply:
    """construct and return a row or column based frame apply object"""
    _, func, columns, _ = reconstruct_func(func, **kwargs)

    axis = obj._get_axis_number(axis)
    klass: type[FrameApply]
    if axis == 0:
        klass = FrameRowApply
    elif axis == 1:
        if columns:
            raise NotImplementedError(
                f"Named aggregation is not supported when {axis=}."
            )
        klass = FrameColumnApply

    return klass(
        obj,
        func,
        raw=raw,
        result_type=result_type,
        by_row=by_row,
        engine=engine,
        engine_kwargs=engine_kwargs,
        args=args,
        kwargs=kwargs,
    )

