
def vlines(
    x: float | ArrayLike,
    ymin: float | ArrayLike,
    ymax: float | ArrayLike,
    colors: ColorType | Sequence[ColorType] | None = None,
    linestyles: LineStyleType = "solid",
    label: str = "",
    *,
    data: DataParamType = None,
    **kwargs,
) -> LineCollection:
    return gca().vlines(
        x,
        ymin,
        ymax,
        colors=colors,
        linestyles=linestyles,
        label=label,
        **({"data": data} if data is not None else {}),
        **kwargs,
    )

