
def ifftshift(x: ArrayLike, axes=None):
    return torch.fft.ifftshift(x, axes)


def ifftshift(input: TensorLikeType, dim: DimsType | None = None) -> TensorLikeType:
    dims = _default_alldims(dim, input)
    shift = [(input.shape[d] + 1) // 2 for d in dims]
    return torch.roll(input, shift, dims)


def ifftshift(x, axes=None):
    """The inverse of `fftshift`. Although identical for even-length `x`, the
    functions differ by one sample for odd-length `x`.

    Parameters
    ----------
    x : array_like
        Input array.
    axes : int or shape tuple, optional
        Axes over which to calculate.  Defaults to None, which shifts all axes.

    Returns
    -------
    y : ndarray
        The shifted array.

    See Also
    --------
    fftshift : Shift zero-frequency component to the center of the spectrum.

    Examples
    --------
    >>> import numpy as np
    >>> freqs = np.fft.fftfreq(9, d=1./9).reshape(3, 3)
    >>> freqs
    array([[ 0.,  1.,  2.],
           [ 3.,  4., -4.],
           [-3., -2., -1.]])
    >>> np.fft.ifftshift(np.fft.fftshift(freqs))
    array([[ 0.,  1.,  2.],
           [ 3.,  4., -4.],
           [-3., -2., -1.]])

    """
    xp = array_namespace(x)
    if hasattr(xp, 'fft'):
        return xp.fft.ifftshift(x, axes=axes)
    x = np.asarray(x)
    y = np.fft.ifftshift(x, axes=axes)
    return xp.asarray(y)


def ifftshift(
    x: Array, /, xp: Namespace, *, axes: int | Sequence[int] | None = None
) -> Array:
    return xp.fft.ifftshift(x, axes=axes)


def ifftshift(
    x: Array,
    /,
    *,
    axes: int | Sequence[int] = None,
    **kwargs: object,
) -> Array:
    return torch.fft.ifftshift(x, dim=axes, **kwargs)


def ifftshift(x, axes=None):
    """
    The inverse of `fftshift`. Although identical for even-length `x`, the
    functions differ by one sample for odd-length `x`.

    Parameters
    ----------
    x : array_like
        Input array.
    axes : int or shape tuple, optional
        Axes over which to calculate.  Defaults to None, which shifts all axes.

    Returns
    -------
    y : ndarray
        The shifted array.

    See Also
    --------
    fftshift : Shift zero-frequency component to the center of the spectrum.

    Examples
    --------
    >>> import numpy as np
    >>> freqs = np.fft.fftfreq(9, d=1./9).reshape(3, 3)
    >>> freqs
    array([[ 0.,  1.,  2.],
           [ 3.,  4., -4.],
           [-3., -2., -1.]])
    >>> np.fft.ifftshift(np.fft.fftshift(freqs))
    array([[ 0.,  1.,  2.],
           [ 3.,  4., -4.],
           [-3., -2., -1.]])

    """
    x = asarray(x)
    if axes is None:
        axes = tuple(range(x.ndim))
        shift = [-(dim // 2) for dim in x.shape]
    elif isinstance(axes, integer_types):
        shift = -(x.shape[axes] // 2)
    else:
        shift = [-(x.shape[ax] // 2) for ax in axes]

    return roll(x, shift, axes)


def ifftshift(x: ArrayLike, axes: None | int | Sequence[int] = None) -> Array:
  """The inverse of :func:`jax.numpy.fft.fftshift`.

  JAX implementation of :func:`numpy.fft.ifftshift`.

  Args:
    x: N-dimensional array array of frequencies.
    axes: optional integer or sequence of integers specifying which axes to
      shift. If None (default), then shift all axes.

  Returns:
    A shifted copy of ``x``.

  See also:
    - :func:`jax.numpy.fft.fftshift`: inverse of ``ifftshift``.
    - :func:`jax.numpy.fft.fftfreq`: generate FFT frequencies.

  Examples:
    Generate FFT frequencies with :func:`~jax.numpy.fft.fftfreq`:

    >>> freq = jnp.fft.fftfreq(5)
    >>> freq
    Array([ 0. ,  0.2,  0.4, -0.4, -0.2], dtype=float32)

    Use :func:`~jax.numpy.fft.fftshift` to shift the zero-frequency entry
    to the middle of the array:

    >>> shifted_freq = jnp.fft.fftshift(freq)
    >>> shifted_freq
    Array([-0.4, -0.2,  0. ,  0.2,  0.4], dtype=float32)

    Unshift with ``ifftshift`` to recover the original frequencies:

    >>> jnp.fft.ifftshift(shifted_freq)
    Array([ 0. ,  0.2,  0.4, -0.4, -0.2], dtype=float32)
  """
  x = ensure_arraylike("ifftshift", x)
  shift: int | Sequence[int]
  if axes is None:
    axes = tuple(range(x.ndim))
    shift = [-(dim // 2) for dim in x.shape]
  elif isinstance(axes, int):
    shift = -(x.shape[axes] // 2)
  else:
    shift = [-(x.shape[ax] // 2) for ax in axes]

  return jnp.roll(x, shift, axes)

