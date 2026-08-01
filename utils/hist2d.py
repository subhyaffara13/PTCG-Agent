
def hist2d(
    x: ArrayLike,
    y: ArrayLike,
    bins: None | int | tuple[int, int] | ArrayLike | tuple[ArrayLike, ArrayLike] = 10,
    range: ArrayLike | None = None,
    density: bool = False,
    weights: ArrayLike | None = None,
    cmin: float | None = None,
    cmax: float | None = None,
    *,
    data: DataParamType = None,
    **kwargs,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, QuadMesh]:
    __ret = gca().hist2d(
        x,
        y,
        bins=bins,
        range=range,
        density=density,
        weights=weights,
        cmin=cmin,
        cmax=cmax,
        **({"data": data} if data is not None else {}),
        **kwargs,
    )
    sci(__ret[-1])
    return __ret

