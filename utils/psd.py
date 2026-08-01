
def psd(x, NFFT=None, Fs=None, detrend=None, window=None,
        noverlap=None, pad_to=None, sides=None, scale_by_freq=None):
    r"""
    Compute the power spectral density.

    The power spectral density :math:`P_{xx}` by Welch's average
    periodogram method.  The vector *x* is divided into *NFFT* length
    segments.  Each segment is detrended by function *detrend* and
    windowed by function *window*.  *noverlap* gives the length of
    the overlap between segments.  The :math:`|\mathrm{fft}(i)|^2`
    of each segment :math:`i` are averaged to compute :math:`P_{xx}`.

    If len(*x*) < *NFFT*, it will be zero padded to *NFFT*.

    Parameters
    ----------
    x : 1-D array or sequence
        Array or sequence containing the data

    %(Spectral)s

    %(PSD)s

    noverlap : int, default: 0 (no overlap)
        The number of points of overlap between segments.

    Returns
    -------
    Pxx : 1-D array
        The values for the power spectrum :math:`P_{xx}` (real valued)

    freqs : 1-D array
        The frequencies corresponding to the elements in *Pxx*

    References
    ----------
    Bendat & Piersol -- Random Data: Analysis and Measurement Procedures, John
    Wiley & Sons (1986)

    See Also
    --------
    specgram
        `specgram` differs in the default overlap; in not returning the mean of
        the segment periodograms; and in returning the times of the segments.

    magnitude_spectrum : returns the magnitude spectrum.

    csd : returns the spectral density between two signals.
    """
    Pxx, freqs = csd(x=x, y=None, NFFT=NFFT, Fs=Fs, detrend=detrend,
                     window=window, noverlap=noverlap, pad_to=pad_to,
                     sides=sides, scale_by_freq=scale_by_freq)
    return Pxx.real, freqs


def psd(
    x: ArrayLike,
    NFFT: int | None = None,
    Fs: float | None = None,
    Fc: int | None = None,
    detrend: (
        Literal["none", "mean", "linear"] | Callable[[ArrayLike], ArrayLike] | None
    ) = None,
    window: Callable[[ArrayLike], ArrayLike] | ArrayLike | None = None,
    noverlap: int | None = None,
    pad_to: int | None = None,
    sides: Literal["default", "onesided", "twosided"] | None = None,
    scale_by_freq: bool | None = None,
    return_line: bool | None = None,
    *,
    data: DataParamType = None,
    **kwargs,
) -> tuple[np.ndarray, np.ndarray] | tuple[np.ndarray, np.ndarray, Line2D]:
    return gca().psd(
        x,
        NFFT=NFFT,
        Fs=Fs,
        Fc=Fc,
        detrend=detrend,
        window=window,
        noverlap=noverlap,
        pad_to=pad_to,
        sides=sides,
        scale_by_freq=scale_by_freq,
        return_line=return_line,
        **({"data": data} if data is not None else {}),
        **kwargs,
    )

