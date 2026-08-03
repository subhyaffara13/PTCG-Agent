from typing import Callable

def csd(x, y, NFFT=None, Fs=None, detrend=None, window=None,
        noverlap=None, pad_to=None, sides=None, scale_by_freq=None):
    """
    Compute the cross-spectral density.

    The cross spectral density :math:`P_{xy}` by Welch's average
    periodogram method.  The vectors *x* and *y* are divided into
    *NFFT* length segments.  Each segment is detrended by function
    *detrend* and windowed by function *window*.  *noverlap* gives
    the length of the overlap between segments.  The product of
    the direct FFTs of *x* and *y* are averaged over each segment
    to compute :math:`P_{xy}`, with a scaling to correct for power
    loss due to windowing.

    If len(*x*) < *NFFT* or len(*y*) < *NFFT*, they will be zero
    padded to *NFFT*.

    Parameters
    ----------
    x, y : 1-D arrays or sequences
        Arrays or sequences containing the data

    %(Spectral)s

    %(PSD)s

    noverlap : int, default: 0 (no overlap)
        The number of points of overlap between segments.

    Returns
    -------
    Pxy : 1-D array
        The values for the cross spectrum :math:`P_{xy}` before scaling (real
        valued)

    freqs : 1-D array
        The frequencies corresponding to the elements in *Pxy*

    References
    ----------
    Bendat & Piersol -- Random Data: Analysis and Measurement Procedures, John
    Wiley & Sons (1986)

    See Also
    --------
    psd : equivalent to setting ``y = x``.
    """
    if NFFT is None:
        NFFT = 256
    Pxy, freqs, _ = _spectral_helper(x=x, y=y, NFFT=NFFT, Fs=Fs,
                                     detrend_func=detrend, window=window,
                                     noverlap=noverlap, pad_to=pad_to,
                                     sides=sides, scale_by_freq=scale_by_freq,
                                     mode='psd')

    if Pxy.ndim == 2:
        if Pxy.shape[1] > 1:
            Pxy = Pxy.mean(axis=1)
        else:
            Pxy = Pxy[:, 0]
    return Pxy, freqs


def csd(
    x: ArrayLike,
    y: ArrayLike,
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
    return gca().csd(
        x,
        y,
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


def csd(x, y, fs=1.0, window='hann_periodic', nperseg=None, noverlap=None, nfft=None,
        detrend='constant', return_onesided=True, scaling='density',
        axis=-1, average='mean'):
    r"""
    Estimate the cross power spectral density, Pxy, using Welch's method.

    Parameters
    ----------
    x : array_like
        Time series of measurement values
    y : array_like
        Time series of measurement values
    fs : float, optional
        Sampling frequency of the `x` and `y` time series. Defaults
        to 1.0.
    window : str or tuple or array_like, optional
        Desired window to use. If `window` is a string or tuple, it is
        passed to `get_window` to generate the window values, which are
        DFT-even by default. See `get_window` for a list of windows and
        required parameters. If `window` is array_like it will be used
        directly as the window and its length must be nperseg. Defaults
        to a periodic Hann window.
    nperseg : int, optional
        Length of each segment. Defaults to None, but if window is str or
        tuple, is set to 256, and if window is array_like, is set to the
        length of the window.
    noverlap : int, optional
        Number of points to overlap between segments. If `None`,
        ``noverlap = nperseg // 2``. Defaults to `None` and may
        not be greater than `nperseg`.
    nfft : int, optional
        Length of the FFT used, if a zero padded FFT is desired. If
        `None`, the FFT length is `nperseg`. Defaults to `None`.
    detrend : str or function or `False`, optional
        Specifies how to detrend each segment. If `detrend` is a
        string, it is passed as the `type` argument to the `detrend`
        function. If it is a function, it takes a segment and returns a
        detrended segment. If `detrend` is `False`, no detrending is
        done. Defaults to 'constant'.
    return_onesided : bool, optional
        If `True`, return a one-sided spectrum for real data. If
        `False` return a two-sided spectrum. Defaults to `True`, but for
        complex data, a two-sided spectrum is always returned.
    scaling : { 'density', 'spectrum' }, optional
        Selects between computing the cross spectral density ('density')
        where `Pxy` has units of V**2/Hz and computing the cross spectrum
        ('spectrum') where `Pxy` has units of V**2, if `x` and `y` are
        measured in V and `fs` is measured in Hz. Defaults to 'density'
    axis : int, optional
        Axis along which the CSD is computed for both inputs; the
        default is over the last axis (i.e. ``axis=-1``).
    average : { 'mean', 'median' }, optional
        Method to use when averaging periodograms. If the spectrum is
        complex, the average is computed separately for the real and
        imaginary parts. Defaults to 'mean'.

        .. versionadded:: 1.2.0

    Returns
    -------
    f : ndarray
        Array of sample frequencies.
    Pxy : ndarray
        Cross spectral density or cross power spectrum of x,y.

    See Also
    --------
    periodogram: Simple, optionally modified periodogram
    lombscargle: Lomb-Scargle periodogram for unevenly sampled data
    welch: Power spectral density by Welch's method. [Equivalent to
           csd(x,x)]
    coherence: Magnitude squared coherence by Welch's method.

    Notes
    -----
    By convention, Pxy is computed with the conjugate FFT of X
    multiplied by the FFT of Y.

    If the input series differ in length, the shorter series will be
    zero-padded to match.

    An appropriate amount of overlap will depend on the choice of window
    and on your requirements. For the default Hann window an overlap of
    50% is a reasonable trade-off between accurately estimating the
    signal power, while not over counting any of the data. Narrower
    windows may require a larger overlap.

    The ratio of the cross spectrum (``scaling='spectrum'``) divided by the cross
    spectral density (``scaling='density'``) is the constant factor of
    ``sum(abs(window)**2)*fs / abs(sum(window))**2``.
    If `return_onesided` is ``True``, the values of the negative frequencies are added
    to values of the corresponding positive ones.

    Consult the :ref:`tutorial_SpectralAnalysis` section of the :ref:`user_guide`
    for a discussion of the scalings of a spectral density and an (amplitude) spectrum.

    Welch's method may be interpreted as taking the average over the time slices of a
    (cross-) spectrogram. Internally, this function utilizes the  `ShortTimeFFT`  to
    determine the required (cross-) spectrogram. An example below illustrates that it
    is straightforward to calculate `Pxy` directly with the `ShortTimeFFT`. However,
    there are some notable differences in the behavior of the `ShortTimeFFT`:

    * There is no direct `ShortTimeFFT` equivalent for the `csd` parameter
      combination ``return_onesided=True, scaling='density'``, since
      ``fft_mode='onesided2X'`` requires ``'psd'`` scaling. The is due to `csd`
      returning the doubled squared magnitude in this case, which does not have a
      sensible interpretation.
    * `ShortTimeFFT` uses `float64` / `complex128` internally, which is due to the
      behavior of the utilized `~scipy.fft` module. Thus, those are the dtypes being
      returned. The `csd` function casts the return values to `float32` / `complex64`
      if the input is `float32` / `complex64` as well.
    * The `csd` function calculates ``np.conj(Sx[q,p]) * Sy[q,p]``, whereas
      `~ShortTimeFFT.spectrogram` calculates ``Sx[q,p] * np.conj(Sy[q,p])`` where
      ``Sx[q,p]``, ``Sy[q,p]`` are the STFTs of `x` and `y`. Also, the window
      positioning is different.

    .. versionadded:: 0.16.0

    References
    ----------
    .. [1] P. Welch, "The use of the fast Fourier transform for the
           estimation of power spectra: A method based on time averaging
           over short, modified periodograms", IEEE Trans. Audio
           Electroacoust. vol. 15, pp. 70-73, 1967.
    .. [2] Rabiner, Lawrence R., and B. Gold. "Theory and Application of
           Digital Signal Processing" Prentice-Hall, pp. 414-419, 1975

    Examples
    --------
    The following example plots the cross power spectral density of two signals with
    some common features:

    >>> import numpy as np
    >>> from scipy import signal
    >>> import matplotlib.pyplot as plt
    >>> rng = np.random.default_rng()
    ...
    ... # Generate two test signals with some common features:
    >>> N, fs = 100_000, 10e3  # number of samples and sampling frequency
    >>> amp, freq = 20, 1234.0  # amplitude and frequency of utilized sine signal
    >>> noise_power = 0.001 * fs / 2
    >>> time = np.arange(N) / fs
    >>> b, a = signal.butter(2, 0.25, 'low')
    >>> x = rng.normal(scale=np.sqrt(noise_power), size=time.shape)
    >>> y = signal.lfilter(b, a, x)
    >>> x += amp*np.sin(2*np.pi*freq*time)
    >>> y += rng.normal(scale=0.1*np.sqrt(noise_power), size=time.shape)
    ...
    ... # Compute and plot the magnitude of the cross spectral density:
    >>> nperseg, noverlap, win = 1024, 512, 'hann'
    >>> f, Pxy = signal.csd(x, y, fs, win, nperseg, noverlap)
    >>> fig0, ax0 = plt.subplots(tight_layout=True)
    >>> ax0.set_title(f"CSD ({win.title()}-window, {nperseg=}, {noverlap=})")
    >>> ax0.set(xlabel="Frequency $f$ in kHz", ylabel="CSD Magnitude in V²/Hz")
    >>> ax0.semilogy(f/1e3, np.abs(Pxy))
    >>> ax0.grid()
    >>> plt.show()

    The cross spectral density is calculated by taking the average over the time slices
    of a spectrogram:

    >>> SFT = signal.ShortTimeFFT.from_window('hann', fs, nperseg, noverlap,
    ...                                       scale_to='psd', fft_mode='onesided2X',
    ...                                       phase_shift=None)
    >>> Sxy1 = SFT.spectrogram(y, x, detr='constant', k_offset=nperseg//2,
    ...                        p0=0, p1=(N-noverlap) // SFT.hop)
    >>> Pxy1 = Sxy1.mean(axis=-1)
    >>> np.allclose(Pxy, Pxy1)  # same result as with csd()
    True

    As discussed in the Notes section, the results of using an approach analogous to
    the code snippet above and the `csd` function may deviate due to implementation
    details.

    Note that the code snippet above can be easily adapted to determine other
    statistical properties than the mean value.
    """
    # The following lines are resembling the behavior of the originally utilized
    # `_spectral_helper()` function:
    same_data, axis = y is x, int(axis)
    x = np.asarray(x)

    if not same_data:
        y = np.asarray(y)
        # Check if we can broadcast the outer axes together
        x_outer, y_outer  = list(x.shape), list(y.shape)
        x_outer.pop(axis)
        y_outer.pop(axis)
        try:
            outer_shape = np.broadcast_shapes(x_outer, y_outer)
        except ValueError as e:
            raise ValueError('x and y cannot be broadcast together.') from e
        if x.size == 0 or y.size == 0:
            out_shape = outer_shape + (min([x.shape[axis], y.shape[axis]]),)
            empty_out = np.moveaxis(np.empty(out_shape), -1, axis)
            return empty_out, empty_out
        out_dtype = np.result_type(x, y, np.complex64)
    else:  # x is y:
        if x.size == 0:
            return np.empty(x.shape), np.empty(x.shape)
        out_dtype = np.result_type(x, np.complex64)

    n = x.shape[axis] if same_data else max(x.shape[axis], y.shape[axis])
    if isinstance(window, str) or isinstance(window, tuple):
        nperseg = int(nperseg) if nperseg is not None else 256
        if nperseg < 1:
            raise ValueError(f"Parameter {nperseg=} is not a positive integer!")
        elif n < nperseg:
            warnings.warn(f"{nperseg=} is greater than signal length max(len(x), " +
                          f"len(y)) = {n}, using nperseg = {n}", stacklevel=3)
            nperseg = n
        win = get_window(window, nperseg)
    else:
        win = np.asarray(window)
        if nperseg is None:
            nperseg = len(win)
    if nperseg != len(win):
        raise ValueError(f"{nperseg=} does not equal {len(win)=}")

    nfft = int(nfft) if nfft is not None else nperseg
    if nfft < nperseg:
        raise ValueError(f"{nfft=} must be greater than or equal to {nperseg=}!")
    noverlap = int(noverlap) if noverlap is not None else nperseg // 2
    if noverlap >= nperseg:
        raise ValueError(f"{noverlap=} must be less than {nperseg=}!")
    if np.iscomplexobj(x) and return_onesided:
        return_onesided = False

    if x.shape[axis] < y.shape[axis]:  # zero-pad x to shape of y:
        z_shape = list(y.shape)
        z_shape[axis] = y.shape[axis] - x.shape[axis]
        x = np.concatenate((x, np.zeros(z_shape)), axis=axis)
    elif y.shape[axis] < x.shape[axis]:  # zero-pad y to shape of x:
        z_shape = list(x.shape)
        z_shape[axis] = x.shape[axis] - y.shape[axis]
        y = np.concatenate((y, np.zeros(z_shape)), axis=axis)

    # using cast() to make mypy happy:
    fft_mode = cast(FFT_MODE_TYPE, 'onesided' if return_onesided else 'twosided')
    if scaling not in (scales := {'spectrum': 'magnitude', 'density': 'psd'}):
        raise ValueError(f"Parameter {scaling=} not in {scales}!")

    SFT = ShortTimeFFT(win, nperseg - noverlap, fs, fft_mode=fft_mode, mfft=nfft,
                       scale_to=scales[scaling], phase_shift=None)
    # csd() calculates X.conj()*Y instead of X*Y.conj():
    Pxy = SFT.spectrogram(y, x, detr=None if detrend is False else detrend,
                          p0=0, p1=(n - noverlap) // SFT.hop, k_offset=nperseg // 2,
                          axis=axis)

    # Note:
    # 'onesided2X' scaling of ShortTimeFFT conflicts with the
    # scaling='spectrum' parameter, since it doubles the squared magnitude,
    # which in the view of the ShortTimeFFT implementation does not make sense.
    # Hence, the doubling of the square is implemented here:
    if return_onesided:
        f_axis = Pxy.ndim - 1 + axis if axis < 0 else axis
        Pxy = np.moveaxis(Pxy, f_axis, -1)
        Pxy[..., 1:-1 if SFT.mfft % 2 == 0 else None] *= 2
        Pxy = np.moveaxis(Pxy, -1, f_axis)

    # Average over windows.
    if Pxy.shape[-1] > 1:
        if average == 'median':
            # np.median must be passed real arrays for the desired result
            bias = _median_bias(Pxy.shape[-1])
            if np.iscomplexobj(Pxy):
                Pxy = (np.median(np.real(Pxy), axis=-1) +
                       np.median(np.imag(Pxy), axis=-1) * 1j)
            else:
                Pxy = np.median(Pxy, axis=-1)
            Pxy /= bias
        elif average == 'mean':
            Pxy = Pxy.mean(axis=-1)
        else:
            raise ValueError(f"Parameter {average=} must be 'median' or 'mean'!")
    else:
        Pxy = np.reshape(Pxy, Pxy.shape[:-1])

    # cast output type;
    Pxy = Pxy.astype(out_dtype)
    if same_data:
        Pxy = Pxy.real
    return SFT.f, Pxy


def csd(x: Array, y: ArrayLike | None, fs: ArrayLike = 1.0, window: str = 'hann',
        nperseg: int | None = None, noverlap: int | None = None,
        nfft: int | None = None, detrend: str = 'constant',
        return_onesided: bool = True, scaling: str = 'density',
        axis: int = -1, average: str = 'mean') -> tuple[Array, Array]:
  """
  Estimate cross power spectral density (CSD) using Welch's method.

  This is a JAX implementation of :func:`scipy.signal.csd`. It is similar to
  :func:`jax.scipy.signal.welch`, but it operates on two input signals and
  estimates their cross-spectral density instead of the power spectral density
  (PSD).

  Args:
    x: Array representing a time series of input values.
    y: Array representing the second time series of input values, the same length as ``x``
      along the specified ``axis``. If not specified, then assume ``y = x`` and compute
      the PSD ``Pxx`` of ``x`` via Welch's  method.
    fs: Sampling frequency of the inputs (default: 1.0).
    window: Data tapering window to apply to each segment. Can be a window function name,
      a tuple specifying a window length and function, or an array (default: ``'hann'``).
    nperseg: Length of each segment (default: 256).
    noverlap: Number of points to overlap between segments (default: ``nperseg // 2``).
    nfft: Length of the FFT used, if a zero-padded FFT is desired. If ``None`` (default),
      the FFT length is ``nperseg``.
    detrend: Specifies how to detrend each segment. Can be ``False`` (default: no detrending),
      ``'constant'`` (remove mean), ``'linear'`` (remove linear trend), or a callable
      accepting a segment and returning a detrended segment.
    return_onesided: If True (default), return a one-sided spectrum for real inputs.
      If False, return a two-sided spectrum.
    scaling: Selects between computing the power spectral density (``'density'``, default)
      or the power spectrum (``'spectrum'``)
    axis: Axis along which the CSD is computed (default: -1).
    average: The type of averaging to use on the periodograms; one of ``'mean'`` (default)
      or ``'median'``.

  Returns:
    A length-2 tuple of arrays ``(f, Pxy)``. ``f`` is the array of sample frequencies,
    and ``Pxy`` is the cross spectral density of `x` and `y`

  Notes:
    The original SciPy function exhibits slightly different behavior between
    ``csd(x, x)`` and ``csd(x, x.copy())``.  The LAX-backend version is designed
    to follow the latter behavior.  To replicate the former, call this function
    function as ``csd(x, None)``.

  See Also:
    - :func:`jax.scipy.signal.welch`: Power spectral density.
    - :func:`jax.scipy.signal.stft`: Short-time Fourier transform.
  """
  freqs, _, Pxy = _spectral_helper(x, y, fs, window, nperseg, noverlap, nfft,
                                  detrend, return_onesided, scaling, axis,
                                  mode='psd')
  if y is not None:
    Pxy = Pxy + 0j  # Ensure complex output when x is not y

  # Average over windows.
  if Pxy.ndim >= 2 and Pxy.size > 0:
    if Pxy.shape[-1] > 1:
      if average == 'median':
        bias = signal_helper._median_bias(Pxy.shape[-1]).astype(Pxy.dtype)
        if jnp.iscomplexobj(Pxy):
          Pxy = (jnp.median(jnp.real(Pxy), axis=-1)
                  + 1j * jnp.median(jnp.imag(Pxy), axis=-1))
        else:
          Pxy = jnp.median(Pxy, axis=-1)
        Pxy /= bias
      elif average == 'mean':
        Pxy = Pxy.mean(axis=-1)
      else:
        raise ValueError(f'average must be "median" or "mean", got {average}')
    else:
      Pxy = jnp.reshape(Pxy, Pxy.shape[:-1])

  return freqs, Pxy

