
def figimage(
    X: ArrayLike,
    xo: int = 0,
    yo: int = 0,
    alpha: float | None = None,
    norm: str | Normalize | None = None,
    cmap: str | Colormap | None = None,
    vmin: float | None = None,
    vmax: float | None = None,
    origin: Literal["upper", "lower"] | None = None,
    resize: bool = False,
    *,
    colorizer: Colorizer | None = None,
    **kwargs,
) -> FigureImage:
    return gcf().figimage(
        X,
        xo=xo,
        yo=yo,
        alpha=alpha,
        norm=norm,
        cmap=cmap,
        vmin=vmin,
        vmax=vmax,
        origin=origin,
        resize=resize,
        colorizer=colorizer,
        **kwargs,
    )

