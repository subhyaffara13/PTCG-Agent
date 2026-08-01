
def acorr(
    x: ArrayLike, *, data: DataParamType = None, **kwargs
) -> tuple[np.ndarray, np.ndarray, LineCollection | Line2D, Line2D | None]:
    return gca().acorr(x, **({"data": data} if data is not None else {}), **kwargs)

