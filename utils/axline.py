
def axline(
    xy1: tuple[float, float],
    xy2: tuple[float, float] | None = None,
    *,
    slope: float | None = None,
    **kwargs,
) -> AxLine:
    return gca().axline(xy1, xy2=xy2, slope=slope, **kwargs)

