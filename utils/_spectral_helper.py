import sys
import time
from typing import Any, Callable

def _spectral_helper(x, y=None, NFFT=None, Fs=None, detrend_func=None,
                     window=None, noverlap=None, pad_to=None,
                     sides=None, scale_by_freq=None, mode=None):
    """
    Private helper implementing the common parts between the psd, csd,
    spectrogram and complex, magnitude, angle, and phase spectrums.
    """
    if y is None:
        # if y is None use x for y
        same_data = True
    else:
        # The checks for if y is x are so that we can use the same function to
        # implement the core of psd(), csd(), and spectrogram() without doing
        # extra calculations.  We return the unaveraged Pxy, freqs, and t.
        same_data = y is x

    if Fs is None:
        Fs = 2
    if noverlap is None:
        noverlap = 0
    if detrend_func is None:
        detrend_func = detrend_none
    if window is None:
        window = window_hanning

    # if NFFT is set to None use the whole signal
    if NFFT is None:
        NFFT = 256

    if not (0 <= noverlap < NFFT):
        raise ValueError('noverlap must be less than NFFT')

    if mode is None or mode == 'default':
        mode = 'psd'
    _api.check_in_list(
        ['default', 'psd', 'complex', 'magnitude', 'angle', 'phase'],
        mode=mode)

    if not same_data and mode != 'psd':
        raise ValueError("x and y must be equal if mode is not 'psd'")

    # Make sure we're dealing with a numpy array. If y and x were the same
    # object to start with, keep them that way
    x = np.asarray(x)
    if not same_data:
        y = np.asarray(y)

    if sides is None or sides == 'default':
        if np.iscomplexobj(x):
            sides = 'twosided'
        else:
            sides = 'onesided'
    _api.check_in_list(['default', 'onesided', 'twosided'], sides=sides)

    # zero pad x and y up to NFFT if they are shorter than NFFT
    if len(x) < NFFT:
        n = len(x)
        x = np.resize(x, NFFT)
        x[n:] = 0

    if not same_data and len(y) < NFFT:
        n = len(y)
        y = np.resize(y, NFFT)
        y[n:] = 0

    if pad_to is None:
        pad_to = NFFT

    if mode != 'psd':
        scale_by_freq = False
    elif scale_by_freq is None:
        scale_by_freq = True

    # For real x, ignore the negative frequencies unless told otherwise
    if sides == 'twosided':
        numFreqs = pad_to
        if pad_to % 2:
            freqcenter = (pad_to - 1)//2 + 1
        else:
            freqcenter = pad_to//2
        scaling_factor = 1.
    elif sides == 'onesided':
        if pad_to % 2:
            numFreqs = (pad_to + 1)//2
        else:
            numFreqs = pad_to//2 + 1
        scaling_factor = 2.

    if not np.iterable(window):
        window = window(np.ones(NFFT, x.dtype))
    if len(window) != NFFT:
        raise ValueError(
            "The window length must match the data's first dimension")

    if sys.maxsize > 2**32:
        result = np.lib.stride_tricks.sliding_window_view(
            x, NFFT, axis=0)[::NFFT - noverlap].T
    else:
        # The NumPy version on 32-bit will OOM, so use old implementation.
        result = _stride_windows(x, NFFT, noverlap=noverlap)
    result = detrend(result, detrend_func, axis=0)
    result = result * window.reshape((-1, 1))
    result = np.fft.fft(result, n=pad_to, axis=0)[:numFreqs, :]
    freqs = np.fft.fftfreq(pad_to, 1/Fs)[:numFreqs]

    if not same_data:
        # if same_data is False, mode must be 'psd'
        if sys.maxsize > 2**32:
            resultY = np.lib.stride_tricks.sliding_window_view(
                y, NFFT, axis=0)[::NFFT - noverlap].T
        else:
            # The NumPy version on 32-bit will OOM, so use old implementation.
            resultY = _stride_windows(y, NFFT, noverlap=noverlap)
        resultY = detrend(resultY, detrend_func, axis=0)
        resultY = resultY * window.reshape((-1, 1))
        resultY = np.fft.fft(resultY, n=pad_to, axis=0)[:numFreqs, :]
        result = np.conj(result) * resultY
    elif mode == 'psd':
        result = np.conj(result) * result
    elif mode == 'magnitude':
        result = np.abs(result) / window.sum()
    elif mode == 'angle' or mode == 'phase':
        # we unwrap the phase later to handle the onesided vs. twosided case
        result = np.angle(result)
    elif mode == 'complex':
        result /= window.sum()

    if mode == 'psd':

        # Also include scaling factors for one-sided densities and dividing by
        # the sampling frequency, if desired. Scale everything, except the DC
        # component and the NFFT/2 component:

        # if we have an even number of frequencies, don't scale NFFT/2
        if not NFFT % 2:
            slc = slice(1, -1, None)
        # if we have an odd number, just don't scale DC
        else:
            slc = slice(1, None, None)

        result[slc] *= scaling_factor

        # MATLAB divides by the sampling frequency so that density function
        # has units of dB/Hz and can be integrated by the plotted frequency
        # values. Perform the same scaling here.
        if scale_by_freq:
            result /= Fs
            # Scale the spectrum by the norm of the window to compensate for
            # windowing loss; see Bendat & Piersol Sec 11.5.2.
            result /= (window**2).sum()
        else:
            # In this case, preserve power in the segment, not amplitude
            result /= window.sum()**2

    t = np.arange(NFFT/2, len(x) - NFFT/2 + 1, NFFT - noverlap)/Fs

    if sides == 'twosided':
        # center the frequency range at zero
        freqs = np.roll(freqs, -freqcenter, axis=0)
        result = np.roll(result, -freqcenter, axis=0)
    elif not pad_to % 2:
        # get the last value correctly, it is negative otherwise
        freqs[-1] *= -1

    # we unwrap the phase here to handle the onesided vs. twosided case
    if mode == 'phase':
        result = np.unwrap(result, axis=0)

    return result, freqs, t


def _spectral_helper(x, y, fs=1.0, window='hann', nperseg=None, noverlap=None,
                     nfft=None, detrend='constant', return_onesided=True,
                     scaling='density', axis=-1, mode='psd', boundary=None,
                     padded=False):
    """Calculate various forms of windowed FFTs for PSD, CSD, etc.

    .. legacy:: function

        This function is soley used by the legacy functions `spectrogram` and `stft`
        (which are also in this same source file `scipy/signal/_spectral_py.py`).

    This is a helper function that implements the commonality between
    the stft, psd, csd, and spectrogram functions. It is not designed to
    be called externally. The windows are not averaged over; the result
    from each window is returned.

    Parameters
    ----------
    x : array_like
        Array or sequence containing the data to be analyzed.
    y : array_like
        Array or sequence containing the data to be analyzed. If this is
        the same object in memory as `x` (i.e. ``_spectral_helper(x,
        x, ...)``), the extra computations are spared.
    fs : float, optional
        Sampling frequency of the time series. Defaults to 1.0.
    window : str or tuple or array_like, optional
        Desired window to use. If `window` is a string or tuple, it is
        passed to `get_window` to generate the window values, which are
        DFT-even by default. See `get_window` for a list of windows and
        required parameters. If `window` is array_like it will be used
        directly as the window and its length must be nperseg. Defaults
        to a Hann window.
    nperseg : int, optional
        Length of each segment. Defaults to None, but if window is str or
        tuple, is set to 256, and if window is array_like, is set to the
        length of the window.
    noverlap : int, optional
        Number of points to overlap between segments. If `None`,
        ``noverlap = nperseg // 2``. Defaults to `None`.
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
        where `Pxy` has units of V²/Hz and computing the cross
        spectrum ('spectrum') where `Pxy` has units of V², if `x`
        and `y` are measured in V and `fs` is measured in Hz.
        Defaults to 'density'
    axis : int, optional
        Axis along which the FFTs are computed; the default is over the
        last axis (i.e. ``axis=-1``).
    mode: str {'psd', 'stft'}, optional
        Defines what kind of return values are expected. Defaults to
        'psd'.
    boundary : str or None, optional
        Specifies whether the input signal is extended at both ends, and
        how to generate the new values, in order to center the first
        windowed segment on the first input point. This has the benefit
        of enabling reconstruction of the first input point when the
        employed window function starts at zero. Valid options are
        ``['even', 'odd', 'constant', 'zeros', None]``. Defaults to
        `None`.
    padded : bool, optional
        Specifies whether the input signal is zero-padded at the end to
        make the signal fit exactly into an integer number of window
        segments, so that all of the signal is included in the output.
        Defaults to `False`. Padding occurs after boundary extension, if
        `boundary` is not `None`, and `padded` is `True`.

    Returns
    -------
    freqs : ndarray
        Array of sample frequencies.
    t : ndarray
        Array of times corresponding to each data segment
    result : ndarray
        Array of output data, contents dependent on *mode* kwarg.

    Notes
    -----
    Adapted from matplotlib.mlab

    .. versionadded:: 0.16.0
    """
    if mode not in ['psd', 'stft']:
        raise ValueError(f"Unknown value for mode {mode}, must be one of: "
                         "{'psd', 'stft'}")

    boundary_funcs = {'even': even_ext,
                      'odd': odd_ext,
                      'constant': const_ext,
                      'zeros': zero_ext,
                      None: None}

    if boundary not in boundary_funcs:
        raise ValueError(f"Unknown boundary option '{boundary}', "
                         f"must be one of: {list(boundary_funcs.keys())}")

    # If x and y are the same object we can save ourselves some computation.
    same_data = y is x

    if not same_data and mode != 'psd':
        raise ValueError("x and y must be equal if mode is 'stft'")

    axis = int(axis)

    # Ensure we have np.arrays, get outdtype
    x = np.asarray(x)
    if not same_data:
        y = np.asarray(y)
        outdtype = np.result_type(x, y, np.complex64)
    else:
        outdtype = np.result_type(x, np.complex64)

    if not same_data:
        # Check if we can broadcast the outer axes together
        xouter = list(x.shape)
        youter = list(y.shape)
        xouter.pop(axis)
        youter.pop(axis)
        try:
            outershape = np.broadcast(np.empty(xouter), np.empty(youter)).shape
        except ValueError as e:
            raise ValueError('x and y cannot be broadcast together.') from e

    if same_data:
        if x.size == 0:
            return np.empty(x.shape), np.empty(x.shape), np.empty(x.shape)
    else:
        if x.size == 0 or y.size == 0:
            outshape = outershape + (min([x.shape[axis], y.shape[axis]]),)
            emptyout = np.moveaxis(np.empty(outshape), -1, axis)
            return emptyout, emptyout, emptyout

    if x.ndim > 1:
        if axis != -1:
            x = np.moveaxis(x, axis, -1)
            if not same_data and y.ndim > 1:
                y = np.moveaxis(y, axis, -1)

    # Check if x and y are the same length, zero-pad if necessary
    if not same_data:
        if x.shape[-1] != y.shape[-1]:
            if x.shape[-1] < y.shape[-1]:
                pad_shape = list(x.shape)
                pad_shape[-1] = y.shape[-1] - x.shape[-1]
                x = np.concatenate((x, np.zeros(pad_shape)), -1)
            else:
                pad_shape = list(y.shape)
                pad_shape[-1] = x.shape[-1] - y.shape[-1]
                y = np.concatenate((y, np.zeros(pad_shape)), -1)

    if nperseg is not None:  # if specified by user
        nperseg = int(nperseg)
        if nperseg < 1:
            raise ValueError('nperseg must be a positive integer')

    # parse window; if array like, then set nperseg = win.shape
    win, nperseg = _triage_segments(window, nperseg, input_length=x.shape[-1])

    if nfft is None:
        nfft = nperseg
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

    # Padding occurs after boundary extension, so that the extended signal ends
    # in zeros, instead of introducing an impulse at the end.
    # I.e. if x = [..., 3, 2]
    # extend then pad -> [..., 3, 2, 2, 3, 0, 0, 0]
    # pad then extend -> [..., 3, 2, 0, 0, 0, 2, 3]

    if boundary is not None:
        ext_func = boundary_funcs[boundary]
        x = ext_func(x, nperseg//2, axis=-1)
        if not same_data:
            y = ext_func(y, nperseg//2, axis=-1)

    if padded:
        # Pad to integer number of windowed segments
        # I.e. make x.shape[-1] = nperseg + (nseg-1)*nstep, with integer nseg
        nadd = (-(x.shape[-1]-nperseg) % nstep) % nperseg
        zeros_shape = list(x.shape[:-1]) + [nadd]
        x = np.concatenate((x, np.zeros(zeros_shape)), axis=-1)
        if not same_data:
            zeros_shape = list(y.shape[:-1]) + [nadd]
            y = np.concatenate((y, np.zeros(zeros_shape)), axis=-1)

    # Handle detrending and window functions
    if not detrend:
        def detrend_func(d):
            return d
    elif not hasattr(detrend, '__call__'):
        def detrend_func(d):
            return _signaltools.detrend(d, type=detrend, axis=-1)
    elif axis != -1:
        # Wrap this function so that it receives a shape that it could
        # reasonably expect to receive.
        def detrend_func(d):
            d = np.moveaxis(d, -1, axis)
            d = detrend(d)
            return np.moveaxis(d, axis, -1)
    else:
        detrend_func = detrend

    if np.result_type(win, np.complex64) != outdtype:
        win = win.astype(outdtype)

    if scaling == 'density':
        scale = 1.0 / (fs * (win*win).sum())
    elif scaling == 'spectrum':
        scale = 1.0 / win.sum()**2
    else:
        raise ValueError(f'Unknown scaling: {scaling!r}')

    if mode == 'stft':
        scale = np.sqrt(scale)

    if return_onesided:
        if np.iscomplexobj(x):
            sides = 'twosided'
            warnings.warn('Input data is complex, switching to return_onesided=False',
                          stacklevel=3)
        else:
            sides = 'onesided'
            if not same_data:
                if np.iscomplexobj(y):
                    sides = 'twosided'
                    warnings.warn('Input data is complex, switching to '
                                  'return_onesided=False',
                                  stacklevel=3)
    else:
        sides = 'twosided'

    if sides == 'twosided':
        freqs = sp_fft.fftfreq(nfft, 1/fs)
    elif sides == 'onesided':
        freqs = sp_fft.rfftfreq(nfft, 1/fs)

    # Perform the windowed FFTs
    result = _fft_helper(x, win, detrend_func, nperseg, noverlap, nfft, sides)

    if not same_data:
        # All the same operations on the y data
        result_y = _fft_helper(y, win, detrend_func, nperseg, noverlap, nfft,
                               sides)
        result = np.conjugate(result) * result_y
    elif mode == 'psd':
        result = np.conjugate(result) * result

    result *= scale
    if sides == 'onesided' and mode == 'psd':
        if nfft % 2:
            result[..., 1:] *= 2
        else:
            # Last point is unpaired Nyquist freq point, don't double
            result[..., 1:-1] *= 2

    time = np.arange(nperseg/2, x.shape[-1] - nperseg/2 + 1,
                     nperseg - noverlap)/float(fs)
    if boundary is not None:
        time -= (nperseg/2) / fs

    result = result.astype(outdtype)

    # All imaginary parts are zero anyways
    if same_data and mode != 'stft':
        result = result.real

    # Output is going to have new last axis for time/window index, so a
    # negative axis index shifts down one
    if axis < 0:
        axis -= 1

    # Roll frequency axis back to axis where the data came from
    result = np.moveaxis(result, -1, axis)

    return freqs, time, result


def _spectral_helper(x: Array, y: ArrayLike | None, fs: ArrayLike = 1.0,
                     window: str = 'hann', nperseg: int | None = None,
                     noverlap: int | None = None, nfft: int | None = None,
                     detrend_type: bool | str | Callable[[Array], Array] = 'constant',
                     return_onesided: bool = True, scaling: str = 'density',
                     axis: int = -1, mode: str = 'psd', boundary: str | None = None,
                     padded: bool = False) -> tuple[Array, Array, Array]:
  """LAX-backend implementation of `scipy.signal._spectral_helper`.

  Unlike the original helper function, `y` can be None for explicitly
  indicating auto-spectral (non cross-spectral) computation.  In addition to
  this, `detrend` argument is renamed to `detrend_type` for avoiding internal
  name overlap.
  """
  if mode not in ('psd', 'stft'):
    raise ValueError(f"Unknown value for mode {mode}, "
                     "must be one of: ('psd', 'stft')")

  def make_pad(mode, **kwargs):
    def pad(x, n, axis=-1):
      pad_width = [(0, 0) for unused_n in range(x.ndim)]
      pad_width[axis] = (n, n)
      return jnp.pad(x, pad_width, mode, **kwargs)
    return pad

  boundary_funcs = {
      'even': make_pad('reflect'),
      'odd': odd_ext,
      'constant': make_pad('edge'),
      'zeros': make_pad('constant', constant_values=0.0),
      None: lambda x, *args, **kwargs: x
  }

  # Check/ normalize inputs
  if boundary not in boundary_funcs:
    raise ValueError(
        f"Unknown boundary option '{boundary}', "
        f"must be one of: {list(boundary_funcs.keys())}")

  axis = core.concrete_or_error(operator.index, axis, "axis of windowed-FFT")
  axis = canonicalize_axis(axis, x.ndim)

  if y is None:
    check_arraylike('spectral_helper', x)
    x, = promote_dtypes_inexact(x)
    y_arr = x  # place-holder for type checking
    outershape = tuple_delete(x.shape, axis)
  else:
    if mode != 'psd':
      raise ValueError("two-argument mode is available only when mode=='psd'")
    check_arraylike('spectral_helper', x, y)
    x, y_arr = promote_dtypes_inexact(x, y)
    if x.ndim != y_arr.ndim:
      raise ValueError("two-arguments must have the same rank ({x.ndim} vs {y.ndim}).")
    # Check if we can broadcast the outer axes together
    try:
      outershape = jnp.broadcast_shapes(tuple_delete(x.shape, axis),
                                        tuple_delete(y_arr.shape, axis))
    except ValueError as err:
      raise ValueError('x and y cannot be broadcast together.') from err

  result_dtype = dtypes.to_complex_dtype(x.dtype)
  freq_dtype = np.finfo(result_dtype).dtype

  nperseg_int: int = 0
  nfft_int: int = 0
  noverlap_int: int = 0

  if nperseg is not None:  # if specified by user
    nperseg_int = core.concrete_or_error(
        int, nperseg, "nperseg of windowed-FFT")
    if nperseg_int < 1:
      raise ValueError('nperseg must be a positive integer')
  # parse window; if array like, then set nperseg = win.shape
  win, nperseg_int = signal_helper._triage_segments(
      window, nperseg if nperseg is None else nperseg_int,
      input_length=x.shape[axis], dtype=x.dtype)

  if noverlap is None:
    noverlap_int = nperseg_int // 2
  else:
    noverlap_int = core.concrete_or_error(
        int, noverlap, "noverlap of windowed-FFT")

  if nfft is None:
    nfft_int = nperseg_int
  else:
    nfft_int = core.concrete_or_error(int, nfft, "nfft of windowed-FFT")

  # Special cases for size == 0
  if y is None:
    if x.size == 0:
      return jnp.zeros(x.shape, freq_dtype), jnp.zeros(x.shape, freq_dtype), jnp.zeros(x.shape, result_dtype)
  else:
    if x.size == 0 or y_arr.size == 0:
      shape = tuple_insert(outershape, min(x.shape[axis], y_arr.shape[axis]), axis)
      return jnp.zeros(shape, freq_dtype), jnp.zeros(shape, freq_dtype), jnp.zeros(shape, result_dtype)

  # Move time-axis to the end
  x = jnp.moveaxis(x, axis, -1)
  if y is not None and y_arr.ndim > 1:
    y_arr = jnp.moveaxis(y_arr, axis, -1)

  # Check if x and y are the same length, zero-pad if necessary
  if y is not None and x.shape[-1] != y_arr.shape[-1]:
    if x.shape[-1] < y_arr.shape[-1]:
      pad_shape = list(x.shape)
      pad_shape[-1] = y_arr.shape[-1] - x.shape[-1]
      x = jnp.concatenate((x, jnp.zeros_like(x, shape=pad_shape)), -1)
    else:
      pad_shape = list(y_arr.shape)
      pad_shape[-1] = x.shape[-1] - y_arr.shape[-1]
      y_arr = jnp.concatenate((y_arr, jnp.zeros_like(x, shape=pad_shape)), -1)

  if nfft_int < nperseg_int:
    raise ValueError('nfft must be greater than or equal to nperseg.')
  if noverlap_int >= nperseg_int:
    raise ValueError('noverlap must be less than nperseg.')
  nstep = nperseg_int - noverlap_int

  # Apply paddings
  if boundary is not None:
    ext_func = boundary_funcs[boundary]
    x = ext_func(x, nperseg_int // 2, axis=-1)
    if y is not None:
      y_arr = ext_func(y_arr, nperseg_int // 2, axis=-1)

  if padded:
    # Pad to integer number of windowed segments
    # I.e make x.shape[-1] = nperseg + (nseg-1)*nstep, with integer nseg
    nadd = (-(x.shape[-1]-nperseg_int) % nstep) % nperseg_int
    x = jnp.concatenate((x, jnp.zeros_like(x, shape=(*x.shape[:-1], nadd))), axis=-1)
    if y is not None:
      y_arr = jnp.concatenate((y_arr, jnp.zeros_like(x, shape=(*y_arr.shape[:-1], nadd))), axis=-1)

  # Handle detrending and window functions
  detrend_func: Any
  if isinstance(detrend_type, str):
    detrend_func = partial(detrend, type=detrend_type, axis=-1)
  elif callable(detrend_type):
    if axis != -1:
      # Wrap this function so that it receives a shape that it could
      # reasonably expect to receive.
      def detrend_func(d):
        d = jnp.moveaxis(d, axis, -1)
        d = detrend_type(d)
        return jnp.moveaxis(d, -1, axis)
    else:
      detrend_func = detrend_type
  elif not detrend_type:
    detrend_func = lambda d: d
  else:
    raise ValueError(f'Unsupported detrend type: {detrend_type}')

  # Determine scale
  if scaling == 'density':
    scale = 1.0 / (fs * (win * win).sum())
  elif scaling == 'spectrum':
    scale = 1.0 / win.sum()**2
  else:
    raise ValueError(f'Unknown scaling: {scaling}')
  if mode == 'stft':
    scale = jnp.sqrt(scale)
  scale, = promote_dtypes_complex(scale)

  # Determine onesided/ two-sided
  if return_onesided:
    sides = 'onesided'
    if jnp.iscomplexobj(x) or jnp.iscomplexobj(y):
      sides = 'twosided'
      warnings.warn('Input data is complex, switching to '
                    'return_onesided=False')
  else:
    sides = 'twosided'

  if sides == 'twosided':
    freqs = jnp_fft.fftfreq(nfft_int, 1/fs, dtype=freq_dtype)
  elif sides == 'onesided':
    freqs = jnp_fft.rfftfreq(nfft_int, 1/fs, dtype=freq_dtype)
  else:
    raise ValueError(f'incorrect value of sides {sides}')

  # Perform the windowed FFTs
  result = _fft_helper(x, win, detrend_func,
                       nperseg_int, noverlap_int, nfft_int, sides)

  if y is not None:
    # All the same operations on the y data
    result_y = _fft_helper(y_arr, win, detrend_func,
                           nperseg_int, noverlap_int, nfft_int, sides)
    result = jnp.conjugate(result) * result_y
  elif mode == 'psd':
    result = jnp.conjugate(result) * result

  result *= scale

  if sides == 'onesided' and mode == 'psd':
    end = None if nfft_int % 2 else -1
    result = result.at[..., 1:end].mul(2)

  time = jnp.arange(nperseg_int / 2, x.shape[-1] - nperseg_int / 2 + 1,
                    nperseg_int - noverlap_int, dtype=freq_dtype) / fs
  if boundary is not None:
    time -= (nperseg_int / 2) / fs

  result = result.astype(result_dtype)

  # All imaginary parts are zero anyways
  if y is None and mode != 'stft':
    result = result.real

  # Move frequency axis back to axis where the data came from
  result = jnp.moveaxis(result, -1, axis)

  return freqs, time, result

