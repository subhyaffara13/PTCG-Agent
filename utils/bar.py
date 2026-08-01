
def bar(
    x: float | ArrayLike,
    height: float | ArrayLike,
    width: float | ArrayLike = 0.8,
    bottom: float | ArrayLike | None = None,
    *,
    align: Literal["center", "edge"] = "center",
    data: DataParamType = None,
    **kwargs,
) -> BarContainer:
    return gca().bar(
        x,
        height,
        width=width,
        bottom=bottom,
        align=align,
        **({"data": data} if data is not None else {}),
        **kwargs,
    )

