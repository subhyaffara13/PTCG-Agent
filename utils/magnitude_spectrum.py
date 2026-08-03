from typing import Callable

def magnitude_spectrum(
    x: ArrayLike,
    Fs: float | None = None,
    Fc: int | None = None,
    window: Callable[[ArrayLike], ArrayLike] | ArrayLike | None = None,
    pad_to: int | None = None,
    sides: Literal["default", "onesided", "twosided"] | None = None,
    scale: Literal["default", "linear", "dB"] | None = None,
    *,
    data: DataParamType = None,
    **kwargs,
) -> tuple[np.ndarray, np.ndarray, Line2D]:
    return gca().magnitude_spectrum(
        x,
        Fs=Fs,
        Fc=Fc,
        window=window,
        pad_to=pad_to,
        sides=sides,
        scale=scale,
        **({"data": data} if data is not None else {}),
        **kwargs,
    )

