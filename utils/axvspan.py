
def axvspan(
    xmin: float, xmax: float, ymin: float = 0, ymax: float = 1, **kwargs
) -> Rectangle:
    return gca().axvspan(xmin, xmax, ymin=ymin, ymax=ymax, **kwargs)

