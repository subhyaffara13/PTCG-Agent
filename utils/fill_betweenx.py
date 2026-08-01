
def fill_betweenx(
    y: ArrayLike,
    x1: ArrayLike | float,
    x2: ArrayLike | float = 0,
    where: Sequence[bool] | None = None,
    step: Literal["pre", "post", "mid"] | None = None,
    interpolate: bool = False,
    *,
    data: DataParamType = None,
    **kwargs,
) -> FillBetweenPolyCollection:
    return gca().fill_betweenx(
        y,
        x1,
        x2=x2,
        where=where,
        step=step,
        interpolate=interpolate,
        **({"data": data} if data is not None else {}),
        **kwargs,
    )

