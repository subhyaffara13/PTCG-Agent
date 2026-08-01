
def hilbert(x, _cache=_cache):
    """
    Return Hilbert transform of a periodic sequence x.

    If x_j and y_j are Fourier coefficients of periodic functions x
    and y, respectively, then::

      y_j = sqrt(-1)*sign(j) * x_j
      y_0 = 0

    Parameters
    ----------
    x : array_like
        The input array, should be periodic.
    _cache : dict, optional
        Dictionary that contains the kernel used to do a convolution with.

    Returns
    -------
    y : ndarray
        The transformed input.

    See Also
    --------
    scipy.signal.hilbert : Compute the analytic signal, using the Hilbert
                           transform.

    Notes
    -----
    If ``sum(x, axis=0) == 0`` then ``hilbert(ihilbert(x)) == x``.

    For even len(x), the Nyquist mode of x is taken zero.

    The sign of the returned transform does not have a factor -1 that is more
    often than not found in the definition of the Hilbert transform. Note also
    that `scipy.signal.hilbert` does have an extra -1 factor compared to this
    function.

    """
    if isinstance(_cache, threading.local):
        if not hasattr(_cache, 'hilbert_cache'):
            _cache.hilbert_cache = {}
        _cache = _cache.hilbert_cache

    tmp = asarray(x)
    if iscomplexobj(tmp):
        return hilbert(tmp.real, _cache) + 1j * hilbert(tmp.imag, _cache)
    n = len(x)
    omega = _cache.get(n)
    if omega is None:
        if len(_cache) > 20:
            while _cache:
                _cache.popitem()

        def kernel(k):
            if k > 0:
                return 1.0
            elif k < 0:
                return -1.0
            return 0.0
        omega = convolve.init_convolution_kernel(n,kernel,d=1)
        _cache[n] = omega
    overwrite_x = _datacopied(tmp, x)
    return convolve.convolve(tmp,omega,swap_real_imag=1,overwrite_x=overwrite_x)


def hilbert(n):
    """
    Create a Hilbert matrix of order `n`.

    Returns the `n` by `n` array with entries `h[i,j] = 1 / (i + j + 1)`.

    Parameters
    ----------
    n : int
        The size of the array to create.

    Returns
    -------
    h : (n, n) ndarray
        The Hilbert matrix.

    See Also
    --------
    invhilbert : Compute the inverse of a Hilbert matrix.

    Notes
    -----
    .. versionadded:: 0.10.0

    Examples
    --------
    >>> from scipy.linalg import hilbert
    >>> hilbert(3)
    array([[ 1.        ,  0.5       ,  0.33333333],
           [ 0.5       ,  0.33333333,  0.25      ],
           [ 0.33333333,  0.25      ,  0.2       ]])

    """
    values = 1.0 / (1.0 + np.arange(2 * n - 1))
    h = hankel(values[:n], r=values[n - 1:])
    return h


def hilbert(x, N=None, axis=-1):
    r"""FFT-based computation of the analytic signal.

    The analytic signal is calculated by zeroing out the negative frequencies and
    doubling the amplitudes of the positive frequencies in the FFT domain.
    The imaginary part of the result is the hilbert transform of the real-valued input
    signal.

    The transformation is done along the last axis by default.

    For numpy arrays, `scipy.fft.set_workers` can be used to change the number of
    workers used for the FFTs.

    Parameters
    ----------
    x : array_like
        Signal data.  Must be real.
    N : int, optional
        Number of output samples. `x` is initially cropped or zero-padded to length
        `N` along `axis`.  Default: ``x.shape[axis]``
    axis : int, optional
        Axis along which to do the transformation.  Default: -1.

    Returns
    -------
    xa : ndarray
        Analytic signal of `x`, of each 1-D array along `axis`

    Notes
    -----
    The analytic signal ``x_a(t)`` of a real-valued signal ``x(t)``
    can be expressed as [1]_

    .. math:: x_a = F^{-1}(F(x) 2U) = x + i y\ ,

    where `F` is the Fourier transform, `U` the unit step function,
    and `y` the Hilbert transform of `x`. [2]_

    In other words, the negative half of the frequency spectrum is zeroed
    out, turning the real-valued signal into a complex-valued signal.  The Hilbert
    transformed signal can be obtained from ``np.imag(hilbert(x))``, and the
    original signal from ``np.real(hilbert(x))``.

    References
    ----------
    .. [1] Wikipedia, "Analytic signal".
           https://en.wikipedia.org/wiki/Analytic_signal
    .. [2] Wikipedia, "Hilbert Transform".
           https://en.wikipedia.org/wiki/Hilbert_transform
    .. [3] Leon Cohen, "Time-Frequency Analysis", 1995. Chapter 2.
    .. [4] Alan V. Oppenheim, Ronald W. Schafer. Discrete-Time Signal
           Processing, Third Edition, 2009. Chapter 12.
           ISBN 13: 978-1292-02572-8

    See Also
    --------
    envelope: Compute envelope of a real- or complex-valued signal.

    Examples
    --------
    In this example we use the Hilbert transform to determine the amplitude
    envelope and instantaneous frequency of an amplitude-modulated signal.

    Let's create a chirp of which the frequency increases from 20 Hz to 100 Hz and
    apply an amplitude modulation:

    >>> import numpy as np
    >>> import matplotlib.pyplot as plt
    >>> from scipy.signal import hilbert, chirp
    ...
    >>> duration, fs = 1, 400  # 1 s signal with sampling frequency of 400 Hz
    >>> t = np.arange(int(fs*duration)) / fs  # timestamps of samples
    >>> signal = chirp(t, 20.0, t[-1], 100.0)
    >>> signal *= (1.0 + 0.5 * np.sin(2.0*np.pi*3.0*t) )

    The amplitude envelope is given by the magnitude of the analytic signal. The
    instantaneous frequency can be obtained by differentiating the
    instantaneous phase in respect to time. The instantaneous phase corresponds
    to the phase angle of the analytic signal.

    >>> analytic_signal = hilbert(signal)
    >>> amplitude_envelope = np.abs(analytic_signal)
    >>> instantaneous_phase = np.unwrap(np.angle(analytic_signal))
    >>> instantaneous_frequency = np.diff(instantaneous_phase) / (2.0*np.pi) * fs
    ...
    >>> fig, (ax0, ax1) = plt.subplots(nrows=2, sharex='all', tight_layout=True)
    >>> ax0.set_title("Amplitude-modulated Chirp Signal")
    >>> ax0.set_ylabel("Amplitude")
    >>> ax0.plot(t, signal, label='Signal')
    >>> ax0.plot(t, amplitude_envelope, label='Envelope')
    >>> ax0.legend()
    >>> ax1.set(xlabel="Time in seconds", ylabel="Frequency in Hz", ylim=(0, 120))
    >>> ax1.plot(t[1:], instantaneous_frequency, 'C2-',
    ...          label='Instantaneous Frequency')
    >>> ax1.legend()
    >>> plt.show()

    """
    xp = array_namespace(x)

    x = xp.asarray(x)
    if xp.isdtype(x.dtype, 'complex floating'):
        raise ValueError("x must be real.")

    if N is None:
        N = x.shape[axis]
    if N <= 0:
        raise ValueError("N must be positive.")

    Xf = sp_fft.fft(x, N, axis=axis)
    Xf = xp.moveaxis(Xf, axis, -1)
    if N % 2 == 0:
        Xf = xpx.at(Xf)[..., 1: N // 2].multiply(2.0)
        Xf = xpx.at(Xf)[..., N // 2 + 1:N].set(0.0)
    else:
        Xf = xpx.at(Xf)[..., 1: (N + 1) // 2].multiply(2.0)
        Xf = xpx.at(Xf)[..., (N + 1) // 2:N].set(0.0)

    Xf = xp.moveaxis(Xf, -1, axis)
    x = sp_fft.ifft(Xf, axis=axis)
    return x


def hilbert(n: int) -> Array:
  r"""Create a Hilbert matrix of order n.

  JAX implementation of :func:`scipy.linalg.hilbert`.

  The Hilbert matrix is defined by:

  .. math::

     H_{ij} = \frac{1}{i + j + 1}

  for :math:`1 \le i \le n` and :math:`1 \le j \le n`.

  Args:
    n: the size of the matrix to create.

  Returns:
    A Hilbert matrix of shape ``(n, n)``

  Examples:
    >>> jax.scipy.linalg.hilbert(2)
    Array([[1.        , 0.5       ],
           [0.5       , 0.33333334]], dtype=float32)
    >>> jax.scipy.linalg.hilbert(3)
    Array([[1.        , 0.5       , 0.33333334],
           [0.5       , 0.33333334, 0.25      ],
           [0.33333334, 0.25      , 0.2       ]], dtype=float32)
  """
  a = lax.broadcasted_iota(float, (n, 1), 0)
  return 1/(a + a.T + 1)

