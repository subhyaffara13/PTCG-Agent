
def pcolormesh(
    *args: ArrayLike,
    alpha: float | None = None,
    norm: str | Normalize | None = None,
    cmap: str | Colormap | None = None,
    vmin: float | None = None,
    vmax: float | None = None,
    colorizer: Colorizer | None = None,
    shading: Literal["flat", "nearest", "gouraud", "auto"] | None = None,
    antialiased: bool = False,
    data: DataParamType = None,
    **kwargs,
) -> QuadMesh:
    __ret = gca().pcolormesh(
        *args,
        alpha=alpha,
        norm=norm,
        cmap=cmap,
        vmin=vmin,
        vmax=vmax,
        colorizer=colorizer,
        shading=shading,
        antialiased=antialiased,
        **({"data": data} if data is not None else {}),
        **kwargs,
    )
    sci(__ret)
    return __ret

