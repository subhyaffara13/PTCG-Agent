
def fftshift(x: ArrayLike, axes=None):
    return torch.fft.fftshift(x, axes)


def fftshift(input: TensorLikeType, dim: DimsType | None = None) -> TensorLikeType:
    dims = _default_alldims(dim, input)
    shift = [input.shape[d] // 2 for d in dims]
    return torch.roll(input, shift, dims)


def fftshift(x, axes=None):
    """Shift the zero-frequency component to the center of the spectrum.

    This function swaps half-spaces for all axes listed (defaults to all).
    Note that ``y[0]`` is the Nyquist component only if ``len(x)`` is even.

    Parameters
    ----------
    x : array_like
        Input array.
    axes : int or shape tuple, optional
        Axes over which to shift.  Default is None, which shifts all axes.

    Returns
    -------
    y : ndarray
        The shifted array.

    See Also
    --------
    ifftshift : The inverse of `fftshift`.

    Examples
    --------
    >>> import numpy as np
    >>> freqs = np.fft.fftfreq(10, 0.1)
    >>> freqs
    array([ 0.,  1.,  2., ..., -3., -2., -1.])
    >>> np.fft.fftshift(freqs)
    array([-5., -4., -3., -2., -1.,  0.,  1.,  2.,  3.,  4.])

    Shift the zero-frequency component only along the second axis:

    >>> freqs = np.fft.fftfreq(9, d=1./9).reshape(3, 3)
    >>> freqs
    array([[ 0.,  1.,  2.],
           [ 3.,  4., -4.],
           [-3., -2., -1.]])
    >>> np.fft.fftshift(freqs, axes=(1,))
    array([[ 2.,  0.,  1.],
           [-4.,  3.,  4.],
           [-1., -3., -2.]])

    """
    xp = array_namespace(x)
    if hasattr(xp, 'fft'):
        return xp.fft.fftshift(x, axes=axes)
    x = np.asarray(x)
    y = np.fft.fftshift(x, axes=axes)
    return xp.asarray(y)


def fftshift(
    x: Array, /, xp: Namespace, *, axes: int | Sequence[int] | None = None
) -> Array:
    return xp.fft.fftshift(x, axes=axes)


def fftshift(
    x: Array,
    /,
    *,
    axes: int | Sequence[int] = None,
    **kwargs: object,
) -> Array:
    return torch.fft.fftshift(x, dim=axes, **kwargs)


def fftshift(x, axes=None):
    """
    Shift the zero-frequency component to the center of the spectrum.

    This function swaps half-spaces for all axes listed (defaults to all).
    Note that ``y[0]`` is the Nyquist component only if ``len(x)`` is even.

    Parameters
    ----------
    x : array_like
        Input array.
    axes : int or shape tuple, optional
        Axes over which to shift.  Default is None, which shifts all axes.

    Returns
    -------
    y : ndarray
        The shifted array.

    See Also
    --------
    ifftshift : The inverse of `fftshift`.

    Examples
    --------
    >>> import numpy as np
    >>> freqs = np.fft.fftfreq(10, 0.1)
    >>> freqs
    array([ 0.,  1.,  2., ..., -3., -2., -1.])
    >>> np.fft.fftshift(freqs)
    array([-5., -4., -3., -2., -1.,  0.,  1.,  2.,  3.,  4.])

    Shift the zero-frequency component only along the second axis:

    >>> freqs = np.fft.fftfreq(9, d=1./9).reshape(3, 3)
    >>> freqs
    array([[ 0.,  1.,  2.],
           [ 3.,  4., -4.],
           [-3., -2., -1.]])
    >>> np.fft.fftshift(freqs, axes=(1,))
    array([[ 2.,  0.,  1.],
           [-4.,  3.,  4.],
           [-1., -3., -2.]])

    """
    x = asarray(x)
    if axes is None:
        axes = tuple(range(x.ndim))
        shift = [dim // 2 for dim in x.shape]
    elif isinstance(axes, integer_types):
        shift = x.shape[axes] // 2
    else:
        shift = [x.shape[ax] // 2 for ax in axes]

    return roll(x, shift, axes)


def fftshift(x: ArrayLike, axes: None | int | Sequence[int] = None) -> Array:
  """Shift zero-frequency fft component to the center of the spectrum.

  JAX implementation of :func:`numpy.fft.fftshift`.

  Args:
    x: N-dimensional array array of frequencies.
    axes: optional integer or sequence of integers specifying which axes to
      shift. If None (default), then shift all axes.

  Returns:
    A shifted copy of ``x``.

  See also:
    - :func:`jax.numpy.fft.ifftshift`: inverse of ``fftshift``.
    - :func:`jax.numpy.fft.fftfreq`: generate FFT frequencies.

  Examples:
    Generate FFT frequencies with :func:`~jax.numpy.fft.fftfreq`:

    >>> freq = jnp.fft.fftfreq(5)
    >>> freq
    Array([ 0. ,  0.2,  0.4, -0.4, -0.2], dtype=float32)

    Use ``fftshift`` to shift the zero-frequency entry to the middle of the array:

    >>> shifted_freq = jnp.fft.fftshift(freq)
    >>> shifted_freq
    Array([-0.4, -0.2,  0. ,  0.2,  0.4], dtype=float32)

    Unshift with :func:`~jax.numpy.fft.ifftshift` to recover the original frequencies:

    >>> jnp.fft.ifftshift(shifted_freq)
    Array([ 0. ,  0.2,  0.4, -0.4, -0.2], dtype=float32)
  """
  x = ensure_arraylike("fftshift", x)
  shift: int | Sequence[int]
  if axes is None:
    axes = tuple(range(x.ndim))
    shift = [dim // 2 for dim in x.shape]
  elif isinstance(axes, int):
    shift = x.shape[axes] // 2
  else:
    shift = [x.shape[ax] // 2 for ax in axes]

  return jnp.roll(x, shift, axes)

