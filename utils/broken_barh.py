
def broken_barh(
    xranges: Sequence[tuple[float, float]],
    yrange: tuple[float, float],
    align: Literal["bottom", "center", "top"] = "bottom",
    *,
    data: DataParamType = None,
    **kwargs,
) -> PolyCollection:
    return gca().broken_barh(
        xranges,
        yrange,
        align=align,
        **({"data": data} if data is not None else {}),
        **kwargs,
    )

