
def pcolor(
    *args: ArrayLike,
    shading: Literal["flat", "nearest", "auto"] | None = None,
    alpha: float | None = None,
    norm: str | Normalize | None = None,
    cmap: str | Colormap | None = None,
    vmin: float | None = None,
    vmax: float | None = None,
    colorizer: Colorizer | None = None,
    data: DataParamType = None,
    **kwargs,
) -> Collection:
    __ret = gca().pcolor(
        *args,
        shading=shading,
        alpha=alpha,
        norm=norm,
        cmap=cmap,
        vmin=vmin,
        vmax=vmax,
        colorizer=colorizer,
        **({"data": data} if data is not None else {}),
        **kwargs,
    )
    sci(__ret)
    return __ret

