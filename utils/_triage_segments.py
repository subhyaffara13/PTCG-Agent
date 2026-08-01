
def _triage_segments(window, nperseg, input_length):
    """
    Parses window and nperseg arguments for spectrogram and _spectral_helper.
    This is a helper function, not meant to be called externally.

    .. legacy:: function

        This function is soley used by the legacy functions `spectrogram` and
        `_spectral_helper` (which are also in this file).

    Parameters
    ----------
    window : str, tuple, or ndarray
        If window is specified by a string or tuple and nperseg is not
        specified, nperseg is set to the default of 256 and returns a window of
        that length.
        If instead the window is array_like and nperseg is not specified, then
        nperseg is set to the length of the window. A ValueError is raised if
        the user supplies both an array_like window and a value for nperseg but
        nperseg does not equal the length of the window.

    nperseg : int
        Length of each segment

    input_length: int
        Length of input signal, i.e. x.shape[-1]. Used to test for errors.

    Returns
    -------
    win : ndarray
        window. If function was called with string or tuple than this will hold
        the actual array used as a window.

    nperseg : int
        Length of each segment. If window is str or tuple, nperseg is set to
        256. If window is array_like, nperseg is set to the length of the
        window.
    """
    # parse window; if array like, then set nperseg = win.shape
    if isinstance(window, str) or isinstance(window, tuple):
        # if nperseg not specified
        if nperseg is None:
            nperseg = 256  # then change to default
        if nperseg > input_length:
            warnings.warn(f'nperseg = {nperseg:d} is greater than input length '
                          f' = {input_length:d}, using nperseg = {input_length:d}',
                          stacklevel=3)
            nperseg = input_length
        win = get_window(window, nperseg)
    else:
        win = np.asarray(window)
        if len(win.shape) != 1:
            raise ValueError('window must be 1-D')
        if input_length < win.shape[-1]:
            raise ValueError('window is longer than input signal')
        if nperseg is None:
            nperseg = win.shape[0]
        elif nperseg is not None:
            if nperseg != win.shape[0]:
                raise ValueError("value specified for nperseg is different"
                                 " from length of window")
    return win, nperseg


def _triage_segments(window: ArrayLike | str | tuple[Any, ...], nperseg: int | None,
                     input_length: int, dtype: DTypeLike) -> tuple[Array, int]:
  """
  Parses window and nperseg arguments for spectrogram and _spectral_helper.
  This is a helper function, not meant to be called externally.

  Args:
    window : string, tuple, or ndarray
      If window is specified by a string or tuple and nperseg is not
      specified, nperseg is set to the default of 256 and returns a window of
      that length.
      If instead the window is array_like and nperseg is not specified, then
      nperseg is set to the length of the window. A ValueError is raised if
      the user supplies both an array_like window and a value for nperseg but
      nperseg does not equal the length of the window.
    nperseg : int
      Length of each segment
    input_length: int
      Length of input signal, i.e. x.shape[-1]. Used to test for errors.
    dtype: dtype for window if specified as a string or tuple. Not referenced
      if window is an array.

  Returns:
    win : ndarray
      window. If function was called with string or tuple than this will hold
      the actual array used as a window.
    nperseg : int
      Length of each segment. If window is str or tuple, nperseg is set to
      256. If window is array_like, nperseg is set to the length of the window.
  """
  if isinstance(window, (str, tuple)):
    nperseg_int = input_length if nperseg is None else int(nperseg)
    if nperseg_int > input_length:
      warnings.warn(f'nperseg={nperseg_int} is greater than {input_length=},'
                    f' using nperseg={input_length}')
      nperseg_int = input_length
    if window == 'hann':
      # Implement the default case without scipy
      win = jnp.array([1.0]) if nperseg_int == 1 else jnp.sin(jnp.linspace(0, np.pi, nperseg_int, endpoint=False)) ** 2
    else:
      # TODO(jakevdp): implement get_window() in JAX to remove optional scipy dependency
      try:
        from scipy.signal import get_window  # pyrefly: ignore[missing-import]
      except ImportError as err:
        raise ImportError(f"scipy must be available to use {window=}") from err
      win = get_window(window, nperseg_int)
    win = jnp.array(win, dtype=dtype)
  else:
    win = jnp.asarray(window, dtype=dtype)
    nperseg_int = win.size if nperseg is None else int(nperseg)
    if win.ndim != 1:
      raise ValueError('window must be 1-D')
    if input_length < win.size:
      raise ValueError('window is longer than input signal')
    if nperseg_int != win.size:
      raise ValueError("value specified for nperseg is different from length of window")
  return win, nperseg_int

