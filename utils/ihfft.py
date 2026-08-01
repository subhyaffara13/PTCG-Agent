
def ihfft(a: ArrayLike, n=None, axis=-1, norm=None):
    return torch.fft.ihfft(a, n, dim=axis, norm=norm)


def ihfft(
    input: TensorLikeType,
    n: int | None = None,
    dim: int = -1,
    norm: NormType = None,
) -> TensorLikeType:
    return _fft_r2c("ihfft", input, n, dim, norm, forward=False, onesided=True)


def ihfft(x, n=None, axis=-1, norm=None, overwrite_x=False, workers=None, *,
          plan=None):
    """
    Compute the inverse FFT of a signal that has Hermitian symmetry.

    Parameters
    ----------
    x : array_like
        Input array.
    n : int, optional
        Length of the inverse FFT, the number of points along
        transformation axis in the input to use.  If `n` is smaller than
        the length of the input, the input is cropped. If it is larger,
        the input is padded with zeros. If `n` is not given, the length of
        the input along the axis specified by `axis` is used.
    axis : int, optional
        Axis over which to compute the inverse FFT. If not given, the last
        axis is used.
    norm : {"backward", "ortho", "forward"}, optional
        Normalization mode (see `fft`). Default is "backward".
    overwrite_x : bool, optional
        If True, the contents of `x` can be destroyed; the default is False.
        See `fft` for more details.
    workers : int, optional
        Maximum number of workers to use for parallel computation. If negative,
        the value wraps around from ``os.cpu_count()``.
        See :func:`~scipy.fft.fft` for more details.
    plan : object, optional
        This argument is reserved for passing in a precomputed plan provided
        by downstream FFT vendors. It is currently not used in SciPy.

        .. versionadded:: 1.5.0

    Returns
    -------
    out : complex ndarray
        The truncated or zero-padded input, transformed along the axis
        indicated by `axis`, or the last one if `axis` is not specified.
        The length of the transformed axis is ``n//2 + 1``.

    See Also
    --------
    hfft, irfft

    Notes
    -----
    `hfft`/`ihfft` are a pair analogous to `rfft`/`irfft`, but for the
    opposite case: here, the signal has Hermitian symmetry in the time
    domain and is real in the frequency domain. So, here, it's `hfft`, for
    which you must supply the length of the result if it is to be odd:
    * even: ``ihfft(hfft(a, 2*len(a) - 2) == a``, within roundoff error,
    * odd: ``ihfft(hfft(a, 2*len(a) - 1) == a``, within roundoff error.

    Examples
    --------
    >>> from scipy.fft import ifft, ihfft
    >>> import numpy as np
    >>> spectrum = np.array([ 15, -4, 0, -1, 0, -4])
    >>> ifft(spectrum)
    array([1.+0.j,  2.+0.j,  3.+0.j,  4.+0.j,  3.+0.j,  2.+0.j]) # may vary
    >>> ihfft(spectrum)
    array([ 1.-0.j,  2.-0.j,  3.-0.j,  4.-0.j]) # may vary
    """
    return (Dispatchable(x, np.ndarray),)


def ihfft(x, n=None, axis=-1, norm=None,
          overwrite_x=False, workers=None, *, plan=None):
    return _execute_1D('ihfft', _duccfft.ihfft, x, n=n, axis=axis, norm=norm,
                       overwrite_x=overwrite_x, workers=workers, plan=plan)


def ihfft(
    x: Array,
    /,
    xp: Namespace,
    *,
    n: int | None = None,
    axis: int = -1,
    norm: _Norm = "backward",
) -> Array:
    res = xp.fft.ihfft(x, n=n, axis=axis, norm=norm)
    if x.dtype in [xp.float32, xp.complex64]:
        return res.astype(xp.complex64)
    return res


def ihfft(a, n=None, axis=-1, norm=None, out=None):
    """
    Compute the inverse FFT of a signal that has Hermitian symmetry.

    Parameters
    ----------
    a : array_like
        Input array.
    n : int, optional
        Length of the inverse FFT, the number of points along
        transformation axis in the input to use.  If `n` is smaller than
        the length of the input, the input is cropped.  If it is larger,
        the input is padded with zeros. If `n` is not given, the length of
        the input along the axis specified by `axis` is used.
    axis : int, optional
        Axis over which to compute the inverse FFT. If not given, the last
        axis is used.
    norm : {"backward", "ortho", "forward"}, optional
        Normalization mode (see `numpy.fft`). Default is "backward".
        Indicates which direction of the forward/backward pair of transforms
        is scaled and with what normalization factor.

        .. versionadded:: 1.20.0

            The "backward", "forward" values were added.

    out : complex ndarray, optional
        If provided, the result will be placed in this array. It should be
        of the appropriate shape and dtype.

        .. versionadded:: 2.0.0

    Returns
    -------
    out : complex ndarray
        The truncated or zero-padded input, transformed along the axis
        indicated by `axis`, or the last one if `axis` is not specified.
        The length of the transformed axis is ``n//2 + 1``.

    See also
    --------
    hfft, irfft

    Notes
    -----
    `hfft`/`ihfft` are a pair analogous to `rfft`/`irfft`, but for the
    opposite case: here the signal has Hermitian symmetry in the time
    domain and is real in the frequency domain. So here it's `hfft` for
    which you must supply the length of the result if it is to be odd:

    * even: ``ihfft(hfft(a, 2*len(a) - 2)) == a``, within roundoff error,
    * odd: ``ihfft(hfft(a, 2*len(a) - 1)) == a``, within roundoff error.

    Examples
    --------
    >>> import numpy as np
    >>> spectrum = np.array([ 15, -4, 0, -1, 0, -4])
    >>> np.fft.ifft(spectrum)
    array([1.+0.j,  2.+0.j,  3.+0.j,  4.+0.j,  3.+0.j,  2.+0.j]) # may vary
    >>> np.fft.ihfft(spectrum)
    array([ 1.-0.j,  2.-0.j,  3.-0.j,  4.-0.j]) # may vary

    """
    a = asarray(a)
    if n is None:
        n = a.shape[axis]
    new_norm = _swap_direction(norm)
    out = rfft(a, n, axis, norm=new_norm, out=out)
    return conjugate(out, out=out)


def ihfft(a: ArrayLike, n: int | None = None,
          axis: int = -1, norm: str | None = None) -> Array:
  r"""Compute a 1-D inverse FFT of an array whose spectrum has Hermitian-symmetry.

  JAX implementation of :func:`numpy.fft.ihfft`.

  Args:
    a: input array.
    n: optional, int. Specifies the effective dimension of the input along ``axis``.
      If not specified, it will default to the dimension of input along ``axis``.
    axis: optional, int, default=-1. Specifies the axis along which the transform
      is computed. If not specified, the transform is computed along axis -1.
    norm: optional, string. The normalization mode. "backward", "ortho" and "forward"
      are supported. Default is "backward".

  Returns:
    An array containing one-dimensional discrete Fourier transform of ``a`` by
    exploiting its inherent Hermitian symmetry. The dimension of the array along
    ``axis`` is ``(n/2)+1``, if ``n`` is even and ``(n+1)/2``, if ``n`` is odd.

  See also:
    - :func:`jax.numpy.fft.hfft`: Computes a one-dimensional FFT of an array
      whose spectrum has Hermitian symmetry.
    - :func:`jax.numpy.fft.fft`: Computes a one-dimensional discrete Fourier
      transform.
    - :func:`jax.numpy.fft.rfft`: Computes a one-dimensional discrete Fourier
      transform of a real-valued input.

  Examples:
    >>> x = jnp.array([[1, 3, 5, 7],
    ...                [2, 4, 6, 8]])
    >>> jnp.fft.ihfft(x)
    Array([[ 4.+0.j, -1.-1.j, -1.-0.j],
           [ 5.+0.j, -1.-1.j, -1.-0.j]], dtype=complex64)

    When ``n=4`` and ``axis=0``, dimension of the transform along ``axis 0`` will
    be ``(4/2)+1 =3`` and dimension along other axes will be same as that of input.

    >>> jnp.fft.ihfft(x, n=4, axis=0)
    Array([[ 0.75+0.j ,  1.75+0.j ,  2.75+0.j ,  3.75+0.j ],
           [ 0.25+0.5j,  0.75+1.j ,  1.25+1.5j,  1.75+2.j ],
           [-0.25-0.j , -0.25-0.j , -0.25-0.j , -0.25-0.j ]], dtype=complex64)
  """
  _axis_check_1d('ihfft', axis)
  arr = jnp.asarray(a)
  nn = arr.shape[axis] if n is None else n
  output = _fft_core_1d('ihfft', lax_fft.FftType.RFFT, arr, n=n, axis=axis,
                        norm=norm)
  return ufuncs.conj(output) * (1 / nn)

