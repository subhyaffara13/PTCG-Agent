import time

def istft(
    input: Tensor,
    n_fft: int,
    hop_length: int | None = None,
    win_length: int | None = None,
    window: Tensor | None = None,
    center: bool = True,
    normalized: bool = False,
    onesided: bool | None = None,
    length: int | None = None,
    return_complex=False,
) -> Tensor:
    torch._check(
        window is None or window.device == input.device,
        lambda: (
            f"istft input and window must be on the same device but got self on {input.device}"
            + f" and window on {window.device}"  # type: ignore[union-attr]
        ),
    )

    hop_length_ = hop_length if hop_length is not None else n_fft // 4
    win_length_ = win_length if win_length is not None else n_fft

    torch._check(
        utils.is_complex_dtype(input.dtype),
        lambda: (
            "istft input and window must be on the same device but got self on "
            + f"{input.device} and window on {window.device}"  # type: ignore[union-attr]
        ),
    )
    n_frames = input.size(-1)
    fft_size = input.size(-2)

    expected_output_signal_len = n_fft + hop_length_ * (n_frames - 1)
    torch._check(input.numel() > 0, lambda: "istft input tensor cannot be empty")
    torch._check(
        2 <= input.ndim <= 3,
        lambda: f"istft expected a tensor with 2 or 3 dimensions, but got {input.ndim}",
    )
    onesided_ = onesided if onesided is not None else fft_size != n_fft

    if onesided_:
        torch._check(
            n_fft // 2 + 1 == fft_size,
            lambda: (
                "istft expected the frequency dimension (3rd to the last) of the input tensor "
                + f"to match n_fft / 2 + 1 when onesided=True, but got {fft_size}"
            ),
        )
    else:
        torch._check(
            n_fft == fft_size,
            lambda: (
                "istft expected the frequency dimension (3rd to the last) of the input tensor "
                + f"to match n_fft when onesided=False, but got {fft_size}",
            ),
        )

    torch._check(
        0 < hop_length_ <= win_length_,
        lambda: "istft expected 0 < hop_length <= win_length",
    )
    torch._check(
        0 < win_length_ <= n_fft, lambda: "istft expected 0 < win_length <= n_fft"
    )
    torch._check(
        window is None or window.shape == (win_length_,),
        lambda: "Invalid window shape. window has to be 1D and length of `win_length`",
    )

    if window is None:
        real_dtype = utils.corresponding_real_dtype(input.dtype)
        window_ = torch.ones(win_length_, dtype=real_dtype, device=input.device)
    else:
        window_ = window

    if win_length_ != n_fft:
        left = (n_fft - win_length_) // 2
        window_ = aten.constant_pad_nd(window_, (left, n_fft - win_length_ - left), 0)

    original_ndim = input.ndim
    if input.ndim == 2:
        input = input.unsqueeze(0)

    input = input.transpose(1, 2)
    norm = "ortho" if normalized else None
    if return_complex:
        torch._check(
            not onesided_,
            lambda: "cannot have onesided output if window or input is complex",
        )
        input = torch.fft.ifft(input, dim=-1, norm=norm)
    else:
        torch._check(
            window is None or not utils.is_complex_dtype(window.dtype),
            lambda: "Complex windows are incompatible with return_complex=False",
        )
        if not onesided_:
            input = input.narrow(dim=-1, start=0, length=n_fft // 2 + 1)
        input = torch.fft.irfft(input, dim=-1, norm=norm)

    if input.size(2) != n_fft:
        raise AssertionError(
            f"Expected input.size(2) == n_fft, got {input.size(2)} != {n_fft}"
        )

    y_tmp = input * window_.view([1, 1, n_fft])
    y = aten.unfold_backward(
        y_tmp,
        input_sizes=(y_tmp.size(0), expected_output_signal_len),
        dim=1,
        size=n_fft,
        step=hop_length_,
    )
    window_envelop = aten.unfold_backward(
        window_.pow(2).expand((1, n_frames, n_fft)),
        input_sizes=(y_tmp.size(0), expected_output_signal_len),
        dim=1,
        size=n_fft,
        step=hop_length_,
    )

    if expected_output_signal_len != y.size(1):
        raise AssertionError(
            f"expected_output_signal_len ({expected_output_signal_len}) != y.size(1) ({y.size(1)})"
        )
    if expected_output_signal_len != window_envelop.size(1):
        raise AssertionError(
            f"expected_output_signal_len ({expected_output_signal_len}) != window_envelop.size(1) ({window_envelop.size(1)})"
        )

    start = n_fft // 2 if center else 0
    if length is not None:
        end = start + length
    elif center:
        end = expected_output_signal_len - n_fft // 2
    else:
        end = expected_output_signal_len

    length = max(0, end - start)
    y = y.narrow(dim=1, start=start, length=length)
    window_envelop = window_envelop.narrow(dim=1, start=start, length=length)

    y = y / window_envelop
    if original_ndim == 2:
        y = y.squeeze(0)

    if end > expected_output_signal_len:
        warnings.warn(
            "The length of signal is shorter than the length parameter. Result is being "
            + "padded with zeros in the tail. Please check your center and hop_length settings",
            stacklevel=2,
        )
        y = aten.constant_pad_nd(y, (0, end - expected_output_signal_len), 0)
    return y


def istft(Zxx, fs=1.0, window='hann_periodic', nperseg=None, noverlap=None, nfft=None,
          input_onesided=True, boundary=True, time_axis=-1, freq_axis=-2,
          scaling='spectrum'):
    r"""Perform the inverse Short Time Fourier transform (legacy function).

    .. legacy:: function

        `ShortTimeFFT` is a newer STFT / ISTFT implementation with more
        features. A :ref:`comparison <tutorial_stft_legacy_stft>` between the
        implementations can be found in the :ref:`tutorial_stft` section of the
        :ref:`user_guide`.

    Parameters
    ----------
    Zxx : array_like
        STFT of the signal to be reconstructed. If a purely real array
        is passed, it will be cast to a complex data type.
    fs : float, optional
        Sampling frequency of the time series. Defaults to 1.0.
    window : str or tuple or array_like, optional
        Desired window to use. If `window` is a string or tuple, it is
        passed to `get_window` to generate the window values, which are
        DFT-even by default. See `get_window` for a list of windows and
        required parameters. If `window` is array_like it will be used
        directly as the window and its length must be nperseg. Defaults
        to a periodic Hann window. Must match the window used to generate the
        STFT for faithful inversion.
    nperseg : int, optional
        Number of data points corresponding to each STFT segment. This
        parameter must be specified if the number of data points per
        segment is odd, or if the STFT was padded via ``nfft >
        nperseg``. If `None`, the value depends on the shape of
        `Zxx` and `input_onesided`. If `input_onesided` is `True`,
        ``nperseg=2*(Zxx.shape[freq_axis] - 1)``. Otherwise,
        ``nperseg=Zxx.shape[freq_axis]``. Defaults to `None`.
    noverlap : int, optional
        Number of points to overlap between segments. If `None`, half
        of the segment length. Defaults to `None`. When specified, the
        COLA constraint must be met (see Notes below), and should match
        the parameter used to generate the STFT. Defaults to `None`.
    nfft : int, optional
        Number of FFT points corresponding to each STFT segment. This
        parameter must be specified if the STFT was padded via ``nfft >
        nperseg``. If `None`, the default values are the same as for
        `nperseg`, detailed above, with one exception: if
        `input_onesided` is True and
        ``nperseg==2*Zxx.shape[freq_axis] - 1``, `nfft` also takes on
        that value. This case allows the proper inversion of an
        odd-length unpadded STFT using ``nfft=None``. Defaults to
        `None`.
    input_onesided : bool, optional
        If `True`, interpret the input array as one-sided FFTs, such
        as is returned by `stft` with ``return_onesided=True`` and
        `numpy.fft.rfft`. If `False`, interpret the input as a a
        two-sided FFT. Defaults to `True`.
    boundary : bool, optional
        Specifies whether the input signal was extended at its
        boundaries by supplying a non-`None` ``boundary`` argument to
        `stft`. Defaults to `True`.
    time_axis : int, optional
        Where the time segments of the STFT is located; the default is
        the last axis (i.e. ``axis=-1``).
    freq_axis : int, optional
        Where the frequency axis of the STFT is located; the default is
        the penultimate axis (i.e. ``axis=-2``).
    scaling : {'spectrum', 'psd'}
        The default 'spectrum' scaling allows each frequency line of `Zxx` to
        be interpreted as a magnitude spectrum. The 'psd' option scales each
        line to a power spectral density - it allows to calculate the signal's
        energy by numerically integrating over ``abs(Zxx)**2``.

    Returns
    -------
    t : ndarray
        Array of output data times.
    x : ndarray
        iSTFT of `Zxx`.

    See Also
    --------
    stft: Short Time Fourier Transform
    ShortTimeFFT: Newer STFT/ISTFT implementation providing more features.
    check_COLA: Check whether the Constant OverLap Add (COLA) constraint
                is met
    check_NOLA: Check whether the Nonzero Overlap Add (NOLA) constraint is met

    Notes
    -----
    In order to enable inversion of an STFT via the inverse STFT with
    `istft`, the signal windowing must obey the constraint of "nonzero
    overlap add" (NOLA):

    .. math:: \sum_{t}w^{2}[n-tH] \ne 0

    This ensures that the normalization factors that appear in the denominator
    of the overlap-add reconstruction equation

    .. math:: x[n]=\frac{\sum_{t}x_{t}[n]w[n-tH]}{\sum_{t}w^{2}[n-tH]}

    are not zero. The NOLA constraint can be checked with the `check_NOLA`
    function.

    An STFT which has been modified (via masking or otherwise) is not
    guaranteed to correspond to an exactly realizible signal. This
    function implements the iSTFT via the least-squares estimation
    algorithm detailed in [2]_, which produces a signal that minimizes
    the mean squared error between the STFT of the returned signal and
    the modified STFT.


    .. versionadded:: 0.19.0

    References
    ----------
    .. [1] Oppenheim, Alan V., Ronald W. Schafer, John R. Buck
           "Discrete-Time Signal Processing", Prentice Hall, 1999.
    .. [2] Daniel W. Griffin, Jae S. Lim "Signal Estimation from
           Modified Short-Time Fourier Transform", IEEE 1984,
           10.1109/TASSP.1984.1164317

    Examples
    --------
    >>> import numpy as np
    >>> from scipy import signal
    >>> import matplotlib.pyplot as plt
    >>> rng = np.random.default_rng()

    Generate a test signal, a 2 Vrms sine wave at 50Hz corrupted by
    0.001 V**2/Hz of white noise sampled at 1024 Hz.

    >>> fs = 1024
    >>> N = 10*fs
    >>> nperseg = 512
    >>> amp = 2 * np.sqrt(2)
    >>> noise_power = 0.001 * fs / 2
    >>> time = np.arange(N) / float(fs)
    >>> carrier = amp * np.sin(2*np.pi*50*time)
    >>> noise = rng.normal(scale=np.sqrt(noise_power),
    ...                    size=time.shape)
    >>> x = carrier + noise

    Compute the STFT, and plot its magnitude

    >>> f, t, Zxx = signal.stft(x, fs=fs, nperseg=nperseg)
    >>> plt.figure()
    >>> plt.pcolormesh(t, f, np.abs(Zxx), vmin=0, vmax=amp, shading='gouraud')
    >>> plt.ylim([f[1], f[-1]])
    >>> plt.title('STFT Magnitude')
    >>> plt.ylabel('Frequency [Hz]')
    >>> plt.xlabel('Time [sec]')
    >>> plt.yscale('log')
    >>> plt.show()

    Zero the components that are 10% or less of the carrier magnitude,
    then convert back to a time series via inverse STFT

    >>> Zxx = np.where(np.abs(Zxx) >= amp/10, Zxx, 0)
    >>> _, xrec = signal.istft(Zxx, fs)

    Compare the cleaned signal with the original and true carrier signals.

    >>> plt.figure()
    >>> plt.plot(time, x, time, xrec, time, carrier)
    >>> plt.xlim([2, 2.1])
    >>> plt.xlabel('Time [sec]')
    >>> plt.ylabel('Signal')
    >>> plt.legend(['Carrier + Noise', 'Filtered via STFT', 'True Carrier'])
    >>> plt.show()

    Note that the cleaned signal does not start as abruptly as the original,
    since some of the coefficients of the transient were also removed:

    >>> plt.figure()
    >>> plt.plot(time, x, time, xrec, time, carrier)
    >>> plt.xlim([0, 0.1])
    >>> plt.xlabel('Time [sec]')
    >>> plt.ylabel('Signal')
    >>> plt.legend(['Carrier + Noise', 'Filtered via STFT', 'True Carrier'])
    >>> plt.show()

    """
    # Make sure input is an ndarray of appropriate complex dtype
    Zxx = np.asarray(Zxx) + 0j
    freq_axis = int(freq_axis)
    time_axis = int(time_axis)

    if Zxx.ndim < 2:
        raise ValueError('Input stft must be at least 2d!')

    if freq_axis == time_axis:
        raise ValueError('Must specify differing time and frequency axes!')

    nseg = Zxx.shape[time_axis]

    if input_onesided:
        # Assume even segment length
        n_default = 2*(Zxx.shape[freq_axis] - 1)
    else:
        n_default = Zxx.shape[freq_axis]

    # Check windowing parameters
    if nperseg is None:
        nperseg = n_default
    else:
        nperseg = int(nperseg)
        if nperseg < 1:
            raise ValueError('nperseg must be a positive integer')

    if nfft is None:
        if (input_onesided) and (nperseg == n_default + 1):
            # Odd nperseg, no FFT padding
            nfft = nperseg
        else:
            nfft = n_default
    elif nfft < nperseg:
        raise ValueError('nfft must be greater than or equal to nperseg.')
    else:
        nfft = int(nfft)

    if noverlap is None:
        noverlap = nperseg//2
    else:
        noverlap = int(noverlap)
    if noverlap >= nperseg:
        raise ValueError('noverlap must be less than nperseg.')
    nstep = nperseg - noverlap

    # Rearrange axes if necessary
    if time_axis != Zxx.ndim-1 or freq_axis != Zxx.ndim-2:
        # Turn negative indices to positive for the call to transpose
        if freq_axis < 0:
            freq_axis = Zxx.ndim + freq_axis
        if time_axis < 0:
            time_axis = Zxx.ndim + time_axis
        zouter = list(range(Zxx.ndim))
        for ax in sorted([time_axis, freq_axis], reverse=True):
            zouter.pop(ax)
        Zxx = np.transpose(Zxx, zouter+[freq_axis, time_axis])

    # Get window as array
    if isinstance(window, str) or type(window) is tuple:
        win = get_window(window, nperseg)
    else:
        win = np.asarray(window)
        if len(win.shape) != 1:
            raise ValueError('window must be 1-D')
        if win.shape[0] != nperseg:
            raise ValueError(f'window must have length of {nperseg}')

    ifunc = sp_fft.irfft if input_onesided else sp_fft.ifft
    xsubs = ifunc(Zxx, axis=-2, n=nfft)[..., :nperseg, :]

    # Initialize output and normalization arrays
    outputlength = nperseg + (nseg-1)*nstep
    x = np.zeros(list(Zxx.shape[:-2])+[outputlength], dtype=xsubs.dtype)
    norm = np.zeros(outputlength, dtype=xsubs.dtype)

    if np.result_type(win, xsubs) != xsubs.dtype:
        win = win.astype(xsubs.dtype)

    if scaling == 'spectrum':
        xsubs *= win.sum()
    elif scaling == 'psd':
        xsubs *= np.sqrt(fs * sum(win**2))
    else:
        raise ValueError(f"Parameter {scaling=} not in ['spectrum', 'psd']!")

    # Construct the output from the ifft segments
    # This loop could perhaps be vectorized/strided somehow...
    for ii in range(nseg):
        # Window the ifft
        x[..., ii*nstep:ii*nstep+nperseg] += xsubs[..., ii] * win
        norm[..., ii*nstep:ii*nstep+nperseg] += win**2

    # Remove extension points
    if boundary:
        x = x[..., nperseg//2:-(nperseg//2)]
        norm = norm[..., nperseg//2:-(nperseg//2)]

    # Divide out normalization where non-tiny
    if np.sum(norm > 1e-10) != len(norm):
        warnings.warn(
            "NOLA condition failed, STFT may not be invertible."
            + (" Possibly due to missing boundary" if not boundary else ""),
            stacklevel=2
        )
    x /= np.where(norm > 1e-10, norm, 1.0)

    if input_onesided:
        x = x.real

    # Put axes back
    if x.ndim > 1:
        if time_axis != Zxx.ndim-1:
            if freq_axis < time_axis:
                time_axis -= 1
            x = np.moveaxis(x, -1, time_axis)

    time = np.arange(x.shape[0])/float(fs)
    return time, x


def istft(Zxx: Array, fs: ArrayLike = 1.0, window: str = 'hann',
          nperseg: int | None = None, noverlap: int | None = None,
          nfft: int | None = None, input_onesided: bool = True,
          boundary: bool = True, time_axis: int = -1,
          freq_axis: int = -2) -> tuple[Array, Array]:
  """
  Perform the inverse short-time Fourier transform (ISTFT).

  JAX implementation of :func:`scipy.signal.istft`; computes the inverse of
  :func:`jax.scipy.signal.stft`.

  Args:
    Zxx: STFT of the signal to be reconstructed.
    fs: Sampling frequency of the time series (default: 1.0)
    window: Data tapering window to apply to each segment. Can be a window function name,
      a tuple specifying a window length and function, or an array (default: ``'hann'``).
    nperseg: Number of data points per segment in the STFT. If ``None`` (default), the
      value is determined from the size of ``Zxx``.
    noverlap: Number of points to overlap between segments (default: ``nperseg // 2``).
    nfft: Number of FFT points used in the STFT. If ``None`` (default), the
      value is determined from the size of ``Zxx``.
    input_onesided: If True (default), interpret the input as a one-sided STFT
      (positive frequencies only). If False, interpret the input as a two-sided STFT.
    boundary: If True (default), it is assumed that the input signal was extended at
      its boundaries by ``stft``. If `False`, the input signal is assumed to have been truncated at the boundaries by `stft`.
    time_axis: Axis in `Zxx` corresponding to time segments (default: -1).
    freq_axis: Axis in `Zxx` corresponding to frequency bins (default: -2).

  Returns:
    A length-2 tuple of arrays ``(t, x)``. ``t`` is the Array of signal times, and ``x``
    is the reconstructed time series.

  See Also:
    :func:`jax.scipy.signal.stft`: short-time Fourier transform.

  Examples:
    Demonstrate that this gives the inverse of :func:`~jax.scipy.signal.stft`:

    >>> x = jnp.array([1., 2., 3., 2., 1., 0., 1., 2.])
    >>> f, t, Zxx = jax.scipy.signal.stft(x, nperseg=4)
    >>> print(Zxx)  # doctest: +SKIP
    [[ 1. +0.j   2.5+0.j   1. +0.j   1. +0.j   0.5+0.j ]
     [-0.5+0.5j -1.5+0.j  -0.5-0.5j -0.5+0.5j  0. -0.5j]
     [ 0. +0.j   0.5+0.j   0. +0.j   0. +0.j  -0.5+0.j ]]
    >>> t, x_reconstructed = jax.scipy.signal.istft(Zxx)
    >>> print(x_reconstructed)
    [1. 2. 3. 2. 1. 0. 1. 2.]
  """
  # Input validation
  Zxx = ensure_arraylike("istft", Zxx)
  if Zxx.ndim < 2:
    raise ValueError('Input stft must be at least 2d!')
  freq_axis = canonicalize_axis(freq_axis, Zxx.ndim)
  time_axis = canonicalize_axis(time_axis, Zxx.ndim)
  if freq_axis == time_axis:
    raise ValueError('Must specify differing time and frequency axes!')

  Zxx = jnp.asarray(Zxx, dtype=dtypes.to_complex_dtype(Zxx.dtype))

  n_default = (2 * (Zxx.shape[freq_axis] - 1) if input_onesided
               else Zxx.shape[freq_axis])

  nperseg_int = core.concrete_or_error(int, nperseg or n_default,
                                           "nperseg: segment length of STFT")
  if nperseg_int < 1:
    raise ValueError('nperseg must be a positive integer')

  nfft_int: int = 0
  if nfft is None:
    nfft_int = n_default
    if input_onesided and nperseg_int == n_default + 1:
      nfft_int += 1  # Odd nperseg, no FFT padding
  else:
    nfft_int = core.concrete_or_error(int, nfft, "nfft of STFT")
  if nfft_int < nperseg_int:
    raise ValueError(
        f'FFT length ({nfft_int}) must be longer than nperseg ({nperseg_int}).')

  noverlap_int = core.concrete_or_error(
      int, noverlap or nperseg_int // 2, "noverlap of STFT")
  if noverlap_int >= nperseg_int:
    raise ValueError('noverlap must be less than nperseg.')
  nstep = nperseg_int - noverlap_int

  # Rearrange axes if necessary
  if time_axis != Zxx.ndim - 1 or freq_axis != Zxx.ndim - 2:
    outer_idxs = tuple(
        idx for idx in range(Zxx.ndim) if idx not in {time_axis, freq_axis})
    Zxx = jnp.transpose(Zxx, outer_idxs + (freq_axis, time_axis))

  # Perform IFFT
  ifunc = jnp_fft.irfft if input_onesided else jnp_fft.ifft
  # xsubs: [..., T, N], N is the number of frames, T is the frame length.
  xsubs = ifunc(Zxx, axis=-2, n=nfft)[..., :nperseg_int, :]

  # Get window as array
  if isinstance(window, str) and window == 'hann':
    # Implement the default case without scipy
    win = jnp.array([1.0]) if nperseg_int == 1 else jnp.sin(jnp.linspace(0, np.pi, nperseg_int, endpoint=False)) ** 2
    win = win.astype(xsubs.dtype)
  elif isinstance(window, (str, tuple)):
    # TODO(jakevdp): implement get_window() in JAX to remove optional scipy dependency
    try:
      from scipy.signal import get_window  # pyrefly: ignore[missing-import]
    except ImportError as err:
      raise ImportError(f"scipy must be available to use {window=}") from err
    win = get_window(window, nperseg_int)
    win = jnp.array(win, dtype=xsubs.dtype)
  else:
    win = jnp.asarray(window)
    if len(win.shape) != 1:
      raise ValueError('window must be 1-D')
    if win.shape[0] != nperseg_int:
      raise ValueError(f'window must have length of {nperseg_int}')
  xsubs *= win.sum()  # This takes care of the 'spectrum' scaling

  # make win broadcastable over xsubs
  win = lax.expand_dims(win, (*range(xsubs.ndim - 2), -1))
  x = _overlap_and_add((xsubs * win).swapaxes(-2, -1), nstep)
  win_squared = jnp.repeat((win * win), xsubs.shape[-1], axis=-1)
  norm = _overlap_and_add(win_squared.swapaxes(-2, -1), nstep)

  # Remove extension points
  if boundary:
    x = x[..., nperseg_int//2:-(nperseg_int//2)]
    norm = norm[..., nperseg_int//2:-(nperseg_int//2)]
  x /= jnp.where(norm > 1e-10, norm, 1.0)

  # Put axes back
  if x.ndim > 1:
    if time_axis != Zxx.ndim - 1:
      if freq_axis < time_axis:
        time_axis -= 1
      x = jnp.moveaxis(x, -1, time_axis)

  time = jnp.arange(x.shape[0], dtype=np.finfo(x.dtype).dtype) / fs
  return time, x

