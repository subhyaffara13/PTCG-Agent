
def rfftfreq(n, d=1.0):
    return torch.fft.rfftfreq(n, d)


def rfftfreq(n, d=1.0, *, xp=None, device=None):
    """Return the Discrete Fourier Transform sample frequencies
    (for usage with rfft, irfft).

    The returned float array `f` contains the frequency bin centers in cycles
    per unit of the sample spacing (with zero at the start).  For instance, if
    the sample spacing is in seconds, then the frequency unit is cycles/second.

    Given a window length `n` and a sample spacing `d`::

      f = [0, 1, ...,     n/2-1,     n/2] / (d*n)   if n is even
      f = [0, 1, ..., (n-1)/2-1, (n-1)/2] / (d*n)   if n is odd

    Unlike `fftfreq` (but like `scipy.fftpack.rfftfreq`)
    the Nyquist frequency component is considered to be positive.

    Parameters
    ----------
    n : int
        Window length.
    d : scalar, optional
        Sample spacing (inverse of the sampling rate). Defaults to 1.
    xp : array_namespace, optional
        The namespace for the return array. Default is None, where NumPy is used.
    device : device, optional
        The device for the return array.
        Only valid when `xp.fft.rfftfreq` implements the device parameter.

    Returns
    -------
    f : ndarray
        Array of length ``n//2 + 1`` containing the sample frequencies.

    Examples
    --------
    >>> import numpy as np
    >>> import scipy.fft
    >>> signal = np.array([-2, 8, 6, 4, 1, 0, 3, 5, -3, 4], dtype=float)
    >>> fourier = scipy.fft.rfft(signal)
    >>> n = signal.size
    >>> sample_rate = 100
    >>> freq = scipy.fft.fftfreq(n, d=1./sample_rate)
    >>> freq
    array([  0.,  10.,  20., ..., -30., -20., -10.])
    >>> freq = scipy.fft.rfftfreq(n, d=1./sample_rate)
    >>> freq
    array([  0.,  10.,  20.,  30.,  40.,  50.])

    """
    xp = np if xp is None else xp
    # numpy does not yet support the `device` keyword
    # `xp.__name__ != 'numpy'` should be removed when numpy is compatible
    if hasattr(xp, 'fft') and xp.__name__ != 'numpy':
        return xp.fft.rfftfreq(n, d=d, device=device)
    if device is not None:
        raise ValueError('device parameter is not supported for input array type')
    return np.fft.rfftfreq(n, d=d)


def rfftfreq(n, d=1.0):
    """DFT sample frequencies (for usage with rfft, irfft).

    The returned float array contains the frequency bins in
    cycles/unit (with zero at the start) given a window length `n` and a
    sample spacing `d`::

      f = [0,1,1,2,2,...,n/2-1,n/2-1,n/2]/(d*n)   if n is even
      f = [0,1,1,2,2,...,n/2-1,n/2-1,n/2,n/2]/(d*n)   if n is odd

    Parameters
    ----------
    n : int
        Window length.
    d : scalar, optional
        Sample spacing. Default is 1.

    Returns
    -------
    out : ndarray
        The array of length `n`, containing the sample frequencies.

    Examples
    --------
    >>> import numpy as np
    >>> from scipy import fftpack
    >>> sig = np.array([-2, 8, 6, 4, 1, 0, 3, 5], dtype=float)
    >>> sig_fft = fftpack.rfft(sig)
    >>> n = sig_fft.size
    >>> timestep = 0.1
    >>> freq = fftpack.rfftfreq(n, d=timestep)
    >>> freq
    array([ 0.  ,  1.25,  1.25,  2.5 ,  2.5 ,  3.75,  3.75,  5.  ])

    """
    n = operator.index(n)
    if n < 0:
        raise ValueError(f"n = {n} is not valid. "
                         "n must be a nonnegative integer.")

    return (np.arange(1, n + 1, dtype=int) // 2) / float(n * d)


def rfftfreq(
    n: int,
    /,
    xp: Namespace,
    *,
    d: float = 1.0,
    dtype: DType | None = None,
    device: Device | None = None,
) -> Array:
    if device not in ["cpu", None]:
        raise ValueError(f"Unsupported device {device!r}")
    res = xp.fft.rfftfreq(n, d=d)
    if dtype is not None:
        return res.astype(dtype)
    return res


def rfftfreq(n, d=1.0, device=None):
    """
    Return the Discrete Fourier Transform sample frequencies
    (for usage with rfft, irfft).

    The returned float array `f` contains the frequency bin centers in cycles
    per unit of the sample spacing (with zero at the start).  For instance, if
    the sample spacing is in seconds, then the frequency unit is cycles/second.

    Given a window length `n` and a sample spacing `d`::

      f = [0, 1, ...,     n/2-1,     n/2] / (d*n)   if n is even
      f = [0, 1, ..., (n-1)/2-1, (n-1)/2] / (d*n)   if n is odd

    Unlike `fftfreq` (but like `scipy.fftpack.rfftfreq`)
    the Nyquist frequency component is considered to be positive.

    Parameters
    ----------
    n : int
        Window length.
    d : scalar, optional
        Sample spacing (inverse of the sampling rate). Defaults to 1.
    device : str, optional
        The device on which to place the created array. Default: ``None``.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    f : ndarray
        Array of length ``n//2 + 1`` containing the sample frequencies.

    Examples
    --------
    >>> import numpy as np
    >>> signal = np.array([-2, 8, 6, 4, 1, 0, 3, 5, -3, 4], dtype=np.float64)
    >>> fourier = np.fft.rfft(signal)
    >>> n = signal.size
    >>> sample_rate = 100
    >>> freq = np.fft.fftfreq(n, d=1./sample_rate)
    >>> freq
    array([  0.,  10.,  20., ..., -30., -20., -10.])
    >>> freq = np.fft.rfftfreq(n, d=1./sample_rate)
    >>> freq
    array([  0.,  10.,  20.,  30.,  40.,  50.])

    """
    if not isinstance(n, integer_types):
        raise ValueError("n should be an integer")
    val = 1.0 / (n * d)
    N = n // 2 + 1
    results = arange(0, N, dtype=int, device=device)
    return results * val


def rfftfreq(n: int, d: ArrayLike = 1.0, *, dtype: DTypeLike | None = None,
             device: xla_client.Device | Sharding | None = None) -> Array:
  """Return sample frequencies for the discrete Fourier transform.

  JAX implementation of :func:`numpy.fft.fftfreq`. Returns frequencies appropriate
  for use with the outputs of :func:`~jax.numpy.fft.rfft` and
  :func:`~jax.numpy.fft.irfft`.

  Args:
    n: length of the FFT window
    d: optional scalar sample spacing (default: 1.0)
    dtype: optional dtype of returned frequencies. If not specified, JAX's default
      floating point dtype will be used.
    device: optional :class:`~jax.Device` or :class:`~jax.sharding.Sharding`
      to which the created array will be committed.

  Returns:
    Array of sample frequencies, length ``n // 2 + 1``.

  See also:
    - :func:`jax.numpy.fft.fftfreq`: frequencies for use with
      :func:`~jax.numpy.fft.fft` and :func:`~jax.numpy.fft.ifft`.
  """
  dtype = dtype or dtypes.default_float_dtype()
  if isinstance(n, (list, tuple)):
    raise ValueError(
          "The n argument of jax.numpy.fft.rfftfreq only takes an int. "
          "Got n = %s." % list(n))

  elif isinstance(d, (list, tuple)):
    raise ValueError(
          "The d argument of jax.numpy.fft.rfftfreq only takes a single value. "
          "Got d = %s." % list(d))

  if n % 2 == 0:
    k = jnp.arange(0, n // 2 + 1, dtype=dtype)

  else:
    k = jnp.arange(0, (n - 1) // 2 + 1, dtype=dtype)

  result = k / jnp.array(d * n, dtype=dtype)

  if device is not None:
    return result.to_device(device)
  return result

