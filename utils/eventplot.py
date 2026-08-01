
def eventplot(
    positions: ArrayLike | Sequence[ArrayLike],
    orientation: Literal["horizontal", "vertical"] = "horizontal",
    lineoffsets: float | Sequence[float] = 1,
    linelengths: float | Sequence[float] = 1,
    linewidths: float | Sequence[float] | None = None,
    colors: ColorType | Sequence[ColorType] | None = None,
    alpha: float | Sequence[float] | None = None,
    linestyles: LineStyleType | Sequence[LineStyleType] = "solid",
    *,
    data: DataParamType = None,
    **kwargs,
) -> EventCollection:
    return gca().eventplot(
        positions,
        orientation=orientation,
        lineoffsets=lineoffsets,
        linelengths=linelengths,
        linewidths=linewidths,
        colors=colors,
        alpha=alpha,
        linestyles=linestyles,
        **({"data": data} if data is not None else {}),
        **kwargs,
    )

