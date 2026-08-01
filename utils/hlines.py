
def hlines(
    y: float | ArrayLike,
    xmin: float | ArrayLike,
    xmax: float | ArrayLike,
    colors: ColorType | Sequence[ColorType] | None = None,
    linestyles: LineStyleType = "solid",
    label: str = "",
    *,
    data: DataParamType = None,
    **kwargs,
) -> LineCollection:
    return gca().hlines(
        y,
        xmin,
        xmax,
        colors=colors,
        linestyles=linestyles,
        label=label,
        **({"data": data} if data is not None else {}),
        **kwargs,
    )

