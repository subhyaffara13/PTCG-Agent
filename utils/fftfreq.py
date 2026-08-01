
def fftfreq(n, d=1.0):
    return torch.fft.fftfreq(n, d)


def fftfreq(n, d=1.0, *, xp=None, device=None):
    """Return the Discrete Fourier Transform sample frequencies.

    The returned float array `f` contains the frequency bin centers in cycles
    per unit of the sample spacing (with zero at the start).  For instance, if
    the sample spacing is in seconds, then the frequency unit is cycles/second.

    Given a window length `n` and a sample spacing `d`::

      f = [0, 1, ...,   n/2-1,     -n/2, ..., -1] / (d*n)   if n is even
      f = [0, 1, ..., (n-1)/2, -(n-1)/2, ..., -1] / (d*n)   if n is odd

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
        Only valid when `xp.fft.fftfreq` implements the device parameter.

    Returns
    -------
    f : ndarray
        Array of length `n` containing the sample frequencies.

    Examples
    --------
    >>> import numpy as np
    >>> import scipy.fft
    >>> signal = np.array([-2, 8, 6, 4, 1, 0, 3, 5], dtype=float)
    >>> fourier = scipy.fft.fft(signal)
    >>> n = signal.size
    >>> timestep = 0.1
    >>> freq = scipy.fft.fftfreq(n, d=timestep)
    >>> freq
    array([ 0.  ,  1.25,  2.5 , ..., -3.75, -2.5 , -1.25])

    """
    xp = np if xp is None else xp
    # numpy does not yet support the `device` keyword
    # `xp.__name__ != 'numpy'` should be removed when numpy is compatible
    if hasattr(xp, 'fft') and xp.__name__ != 'numpy':
        return xp.fft.fftfreq(n, d=d, device=device)
    if device is not None:
        raise ValueError('device parameter is not supported for input array type')
    return np.fft.fftfreq(n, d=d)


def fftfreq(
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
    res = xp.fft.fftfreq(n, d=d)
    if dtype is not None:
        return res.astype(dtype)
    return res


def fftfreq(n, d=1.0, device=None):
    """
    Return the Discrete Fourier Transform sample frequencies.

    The returned float array `f` contains the frequency bin centers in cycles
    per unit of the sample spacing (with zero at the start).  For instance, if
    the sample spacing is in seconds, then the frequency unit is cycles/second.

    Given a window length `n` and a sample spacing `d`::

      f = [0, 1, ...,   n/2-1,     -n/2, ..., -1] / (d*n)   if n is even
      f = [0, 1, ..., (n-1)/2, -(n-1)/2, ..., -1] / (d*n)   if n is odd

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
        Array of length `n` containing the sample frequencies.

    Examples
    --------
    >>> import numpy as np
    >>> signal = np.array([-2, 8, 6, 4, 1, 0, 3, 5], dtype=np.float64)
    >>> fourier = np.fft.fft(signal)
    >>> n = signal.size
    >>> timestep = 0.1
    >>> freq = np.fft.fftfreq(n, d=timestep)
    >>> freq
    array([ 0.  ,  1.25,  2.5 , ..., -3.75, -2.5 , -1.25])

    """
    if not isinstance(n, integer_types):
        raise ValueError("n should be an integer")
    val = 1.0 / (n * d)
    results = empty(n, int, device=device)
    N = (n - 1) // 2 + 1
    p1 = arange(0, N, dtype=int, device=device)
    results[:N] = p1
    p2 = arange(-(n // 2), 0, dtype=int, device=device)
    results[N:] = p2
    return results * val


def fftfreq(n: int, d: ArrayLike = 1.0, *, dtype: DTypeLike | None = None,
            device: xla_client.Device | Sharding | None = None) -> Array:
  """Return sample frequencies for the discrete Fourier transform.

  JAX implementation of :func:`numpy.fft.fftfreq`. Returns frequencies appropriate
  for use with the outputs of :func:`~jax.numpy.fft.fft` and :func:`~jax.numpy.fft.ifft`.

  Args:
    n: length of the FFT window
    d: optional scalar sample spacing (default: 1.0)
    dtype: optional dtype of returned frequencies. If not specified, JAX's default
      floating point dtype will be used.
    device: optional :class:`~jax.Device` or :class:`~jax.sharding.Sharding`
      to which the created array will be committed.

  Returns:
    Array of sample frequencies, length ``n``.

  See also:
    - :func:`jax.numpy.fft.rfftfreq`: frequencies for use with
      :func:`~jax.numpy.fft.rfft` and :func:`~jax.numpy.fft.irfft`.
  """
  dtype = dtype or dtypes.default_float_dtype()

  if isinstance(n, (list, tuple)):
    raise ValueError(
          "The n argument of jax.numpy.fft.fftfreq only takes an int. "
          "Got n = %s." % list(n))

  elif isinstance(d, (list, tuple)):
    raise ValueError(
          "The d argument of jax.numpy.fft.fftfreq only takes a single value. "
          "Got d = %s." % list(d))

  out_dtype = dtype
  dtype = dtypes.finfo(dtypes.to_inexact_dtype(dtype)).dtype

  i = jnp.arange(n, dtype=dtype, device=device)
  k = ((i + n//2) % n - n//2)
  result = k.astype(dtype) / jnp.array(d * n, dtype=dtype, device=device)
  return result.astype(out_dtype)

