
def general_cosine(
    M,
    *,
    a: Iterable,
    sym: bool = True,
    dtype: torch.dtype | None = None,
    layout: torch.layout = torch.strided,
    device: torch.device | None = None,
    requires_grad: bool = False,
) -> Tensor:
    if dtype is None:
        dtype = torch.get_default_dtype()

    _window_function_checks("general_cosine", M, dtype, layout)

    if M == 0:
        return torch.empty(
            (0,), dtype=dtype, layout=layout, device=device, requires_grad=requires_grad
        )

    if M == 1:
        return torch.ones(
            (1,), dtype=dtype, layout=layout, device=device, requires_grad=requires_grad
        )

    if not isinstance(a, Iterable):
        raise TypeError("Coefficients must be a list/tuple")

    if not a:
        raise ValueError("Coefficients cannot be empty")

    constant = 2 * torch.pi / (M if not sym else M - 1)

    k = torch.linspace(
        start=0,
        end=(M - 1) * constant,
        steps=M,
        dtype=dtype,
        layout=layout,
        device=device,
        requires_grad=requires_grad,
    )

    a_i = torch.tensor(
        [(-1) ** i * w for i, w in enumerate(a)],
        device=device,
        dtype=dtype,
        requires_grad=requires_grad,
    )
    i = torch.arange(
        a_i.shape[0],
        dtype=a_i.dtype,
        device=a_i.device,
        requires_grad=a_i.requires_grad,
    )
    return (a_i.unsqueeze(-1) * torch.cos(i.unsqueeze(-1) * k)).sum(0)


def general_cosine(M, a, sym=True):
    r"""
    Generic weighted sum of cosine terms window.

    Parameters
    ----------
    M : int
        Number of points in the output window
    a : array_like
        Sequence of weighting coefficients. This uses the convention of being
        centered on the origin, so these will typically all be positive
        numbers, not alternating sign.
    sym : bool, optional
        When True (default), generates a symmetric window, for use in filter
        design.
        When False, generates a periodic window, for use in spectral analysis.

    Returns
    -------
    w : ndarray
        The array of window values.

    References
    ----------
    .. [1] A. Nuttall, "Some windows with very good sidelobe behavior," IEEE
           Transactions on Acoustics, Speech, and Signal Processing, vol. 29,
           no. 1, pp. 84-91, Feb 1981. :doi:`10.1109/TASSP.1981.1163506`.
    .. [2] Heinzel G. et al., "Spectrum and spectral density estimation by the
           Discrete Fourier transform (DFT), including a comprehensive list of
           window functions and some new flat-top windows", February 15, 2002
           https://holometer.fnal.gov/GH_FFT.pdf

    Examples
    --------
    Heinzel describes a flat-top window named "HFT90D" with formula: [2]_

    .. math::  w_j = 1 - 1.942604 \cos(z) + 1.340318 \cos(2z)
               - 0.440811 \cos(3z) + 0.043097 \cos(4z)

    where

    .. math::  z = \frac{2 \pi j}{N}, j = 0...N - 1

    Since this uses the convention of starting at the origin, to reproduce the
    window, we need to convert every other coefficient to a positive number:

    >>> HFT90D = [1, 1.942604, 1.340318, 0.440811, 0.043097]

    The paper states that the highest sidelobe is at -90.2 dB.  Reproduce
    Figure 42 by plotting the window and its frequency response, and confirm
    the sidelobe level in red:

    >>> import numpy as np
    >>> from scipy.signal.windows import general_cosine
    >>> from scipy.fft import fft, fftshift
    >>> import matplotlib.pyplot as plt

    >>> window = general_cosine(1000, HFT90D, sym=False)
    >>> plt.plot(window)
    >>> plt.title("HFT90D window")
    >>> plt.ylabel("Amplitude")
    >>> plt.xlabel("Sample")

    >>> plt.figure()
    >>> A = fft(window, 10000) / (len(window)/2.0)
    >>> freq = np.linspace(-0.5, 0.5, len(A))
    >>> response = np.abs(fftshift(A / abs(A).max()))
    >>> response = 20 * np.log10(np.maximum(response, 1e-10))
    >>> plt.plot(freq, response)
    >>> plt.axis([-50/1000, 50/1000, -140, 0])
    >>> plt.title("Frequency response of the HFT90D window")
    >>> plt.ylabel("Normalized magnitude [dB]")
    >>> plt.xlabel("Normalized frequency [cycles per sample]")
    >>> plt.axhline(-90.2, color='red')
    >>> plt.show()
    """
    xp = array_namespace(a)
    a = xp.asarray(a)
    device = xp_device(a)
    return _general_cosine_impl(M, a, xp, device, sym=sym)

