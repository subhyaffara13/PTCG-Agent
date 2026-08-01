
def general_hamming(
    M,
    *,
    alpha: float = 0.54,
    sym: bool = True,
    dtype: torch.dtype | None = None,
    layout: torch.layout = torch.strided,
    device: torch.device | None = None,
    requires_grad: bool = False,
) -> Tensor:
    return general_cosine(
        M,
        a=[alpha, 1.0 - alpha],
        sym=sym,
        dtype=dtype,
        layout=layout,
        device=device,
        requires_grad=requires_grad,
    )


def general_hamming(M, alpha, sym=True, *, xp=None, device=None):
    r"""Return a generalized Hamming window.

    The generalized Hamming window is constructed by multiplying a rectangular
    window by one period of a cosine function [1]_.

    Parameters
    ----------
    M : int
        Number of points in the output window. If zero, an empty array
        is returned. An exception is thrown when it is negative.
    alpha : float
        The window coefficient, :math:`\alpha`
    sym : bool, optional
        When True (default), generates a symmetric window, for use in filter
        design.
        When False, generates a periodic window, for use in spectral analysis.
    %(xp_device_snippet)s

    Returns
    -------
    w : ndarray
        The window, with the maximum value normalized to 1 (though the value 1
        does not appear if `M` is even and `sym` is True).

    See Also
    --------
    hamming, hann

    Notes
    -----
    The generalized Hamming window is defined as

    .. math:: w(n) = \alpha - \left(1 - \alpha\right)
              \cos\left(\frac{2\pi{n}}{M-1}\right) \qquad 0 \leq n \leq M-1

    Both the common Hamming window and Hann window are special cases of the
    generalized Hamming window with :math:`\alpha` = 0.54 and :math:`\alpha` =
    0.5, respectively [2]_.

    References
    ----------
    .. [1] DSPRelated, "Generalized Hamming Window Family",
           https://www.dsprelated.com/freebooks/sasp/Generalized_Hamming_Window_Family.html
    .. [2] Wikipedia, "Window function",
           https://en.wikipedia.org/wiki/Window_function
    .. [3] Riccardo Piantanida ESA, "Sentinel-1 Level 1 Detailed Algorithm
           Definition",
           https://sentinel.esa.int/documents/247904/1877131/Sentinel-1-Level-1-Detailed-Algorithm-Definition
    .. [4] Matthieu Bourbigot ESA, "Sentinel-1 Product Definition",
           https://sentinel.esa.int/documents/247904/1877131/Sentinel-1-Product-Definition

    Examples
    --------
    The Sentinel-1A/B Instrument Processing Facility uses generalized Hamming
    windows in the processing of spaceborne Synthetic Aperture Radar (SAR)
    data [3]_. The facility uses various values for the :math:`\alpha`
    parameter based on operating mode of the SAR instrument. Some common
    :math:`\alpha` values include 0.75, 0.7 and 0.52 [4]_. As an example, we
    plot these different windows.

    >>> import numpy as np
    >>> from scipy.signal.windows import general_hamming
    >>> from scipy.fft import fft, fftshift
    >>> import matplotlib.pyplot as plt

    >>> fig1, spatial_plot = plt.subplots()
    >>> spatial_plot.set_title("Generalized Hamming Windows")
    >>> spatial_plot.set_ylabel("Amplitude")
    >>> spatial_plot.set_xlabel("Sample")

    >>> fig2, freq_plot = plt.subplots()
    >>> freq_plot.set_title("Frequency Responses")
    >>> freq_plot.set_ylabel("Normalized magnitude [dB]")
    >>> freq_plot.set_xlabel("Normalized frequency [cycles per sample]")

    >>> for alpha in [0.75, 0.7, 0.52]:
    ...     window = general_hamming(41, alpha)
    ...     spatial_plot.plot(window, label="{:.2f}".format(alpha))
    ...     A = fft(window, 2048) / (len(window)/2.0)
    ...     freq = np.linspace(-0.5, 0.5, len(A))
    ...     response = 20 * np.log10(np.abs(fftshift(A / abs(A).max())))
    ...     freq_plot.plot(freq, response, label="{:.2f}".format(alpha))
    >>> freq_plot.legend(loc="upper right")
    >>> spatial_plot.legend(loc="upper right")

    """
    xp = _namespace(xp)
    a = xp.asarray([alpha, 1. - alpha], dtype=xp.float64, device=device)
    device = xp_device(a)
    return _general_cosine_impl(M, a, xp, device, sym=sym)

