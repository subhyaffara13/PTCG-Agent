
def axvline(x: float = 0, ymin: float = 0, ymax: float = 1, **kwargs) -> Line2D:
    return gca().axvline(x=x, ymin=ymin, ymax=ymax, **kwargs)

