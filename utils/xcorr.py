
def xcorr(
    x: ArrayLike,
    y: ArrayLike,
    normed: bool = True,
    detrend: Callable[[ArrayLike], ArrayLike] = mlab.detrend_none,
    usevlines: bool = True,
    maxlags: int = 10,
    *,
    data: DataParamType = None,
    **kwargs,
) -> tuple[np.ndarray, np.ndarray, LineCollection | Line2D, Line2D | None]:
    return gca().xcorr(
        x,
        y,
        normed=normed,
        detrend=detrend,
        usevlines=usevlines,
        maxlags=maxlags,
        **({"data": data} if data is not None else {}),
        **kwargs,
    )

