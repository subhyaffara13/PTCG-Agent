
def set_ticks_props(
    axes: Axes | Iterable[Axes],
    xlabelsize: int | None = None,
    xrot=None,
    ylabelsize: int | None = None,
    yrot=None,
):
    for ax in flatten_axes(axes):
        if xlabelsize is not None:
            mpl.artist.setp(ax.get_xticklabels(), fontsize=xlabelsize)  # type: ignore[arg-type]
        if xrot is not None:
            mpl.artist.setp(ax.get_xticklabels(), rotation=xrot)  # type: ignore[arg-type]
        if ylabelsize is not None:
            mpl.artist.setp(ax.get_yticklabels(), fontsize=ylabelsize)  # type: ignore[arg-type]
        if yrot is not None:
            mpl.artist.setp(ax.get_yticklabels(), rotation=yrot)  # type: ignore[arg-type]
    return axes

