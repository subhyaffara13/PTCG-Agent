
def axhspan(
    ymin: float, ymax: float, xmin: float = 0, xmax: float = 1, **kwargs
) -> Rectangle:
    return gca().axhspan(ymin, ymax, xmin=xmin, xmax=xmax, **kwargs)

