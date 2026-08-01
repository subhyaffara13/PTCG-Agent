
def barh(
    y: float | ArrayLike,
    width: float | ArrayLike,
    height: float | ArrayLike = 0.8,
    left: float | ArrayLike | None = None,
    *,
    align: Literal["center", "edge"] = "center",
    data: DataParamType = None,
    **kwargs,
) -> BarContainer:
    return gca().barh(
        y,
        width,
        height=height,
        left=left,
        align=align,
        **({"data": data} if data is not None else {}),
        **kwargs,
    )

