
def colorbar(
    mappable: ScalarMappable | ColorizingArtist | None = None,
    cax: matplotlib.axes.Axes | None = None,
    ax: matplotlib.axes.Axes | Iterable[matplotlib.axes.Axes] | None = None,
    **kwargs
) -> Colorbar:
    if mappable is None:
        mappable = gci()
        if mappable is None:
            raise RuntimeError('No mappable was found to use for colorbar '
                               'creation. First define a mappable such as '
                               'an image (with imshow) or a contour set ('
                               'with contourf).')
    ret = gcf().colorbar(mappable, cax=cax, ax=ax, **kwargs)
    return ret

