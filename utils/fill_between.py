
def fill_between(
    x: ArrayLike,
    y1: ArrayLike | float,
    y2: ArrayLike | float = 0,
    where: Sequence[bool] | None = None,
    interpolate: bool = False,
    step: Literal["pre", "post", "mid"] | None = None,
    *,
    data: DataParamType = None,
    **kwargs,
) -> FillBetweenPolyCollection:
    return gca().fill_between(
        x,
        y1,
        y2=y2,
        where=where,
        interpolate=interpolate,
        step=step,
        **({"data": data} if data is not None else {}),
        **kwargs,
    )

