
def hfft(a: ArrayLike, n=None, axis=-1, norm=None):
    return torch.fft.hfft(a, n, dim=axis, norm=norm)


def hfft(
    input: TensorLikeType,
    n: int | None = None,
    dim: int = -1,
    norm: NormType = None,
) -> TensorLikeType:
    return _fft_c2r("hfft", input, n, dim, norm, forward=True)


def hfft(x, n=None, axis=-1, norm=None, overwrite_x=False, workers=None, *,
         plan=None):
    """
    Compute the FFT of a signal that has Hermitian symmetry, i.e., a real
    spectrum.

    Parameters
    ----------
    x : array_like
        The input array.
    n : int, optional
        Length of the transformed axis of the output. For `n` output
        points, ``n//2 + 1`` input points are necessary. If the input is
        longer than this, it is cropped. If it is shorter than this, it is
        padded with zeros. If `n` is not given, it is taken to be ``2*(m-1)``,
        where ``m`` is the length of the input along the axis specified by
        `axis`.
    axis : int, optional
        Axis over which to compute the FFT. If not given, the last
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
    out : ndarray
        The truncated or zero-padded input, transformed along the axis
        indicated by `axis`, or the last one if `axis` is not specified.
        The length of the transformed axis is `n`, or, if `n` is not given,
        ``2*m - 2``, where ``m`` is the length of the transformed axis of
        the input. To get an odd number of output points, `n` must be
        specified, for instance, as ``2*m - 1`` in the typical case,

    Raises
    ------
    IndexError
        If `axis` is larger than the last axis of `a`.

    See Also
    --------
    rfft : Compute the 1-D FFT for real input.
    ihfft : The inverse of `hfft`.
    hfftn : Compute the N-D FFT of a Hermitian signal.

    Notes
    -----
    `hfft`/`ihfft` are a pair analogous to `rfft`/`irfft`, but for the
    opposite case: here the signal has Hermitian symmetry in the time
    domain and is real in the frequency domain. So, here, it's `hfft`, for
    which you must supply the length of the result if it is to be odd.
    * even: ``ihfft(hfft(a, 2*len(a) - 2) == a``, within roundoff error,
    * odd: ``ihfft(hfft(a, 2*len(a) - 1) == a``, within roundoff error.

    Examples
    --------
    >>> from scipy.fft import fft, hfft
    >>> import numpy as np
    >>> a = 2 * np.pi * np.arange(10) / 10
    >>> signal = np.cos(a) + 3j * np.sin(3 * a)
    >>> fft(signal).round(10)
    array([ -0.+0.j,   5.+0.j,  -0.+0.j,  15.-0.j,   0.+0.j,   0.+0.j,
            -0.+0.j, -15.-0.j,   0.+0.j,   5.+0.j])
    >>> hfft(signal[:6]).round(10) # Input first half of signal
    array([  0.,   5.,   0.,  15.,  -0.,   0.,   0., -15.,  -0.,   5.])
    >>> hfft(signal, 10)  # Input entire signal and truncate
    array([  0.,   5.,   0.,  15.,  -0.,   0.,   0., -15.,  -0.,   5.])
    """
    return (Dispatchable(x, np.ndarray),)


def hfft(x, n=None, axis=-1, norm=None,
         overwrite_x=False, workers=None, *, plan=None):
    return _execute_1D('hfft', _duccfft.hfft, x, n=n, axis=axis, norm=norm,
                       overwrite_x=overwrite_x, workers=workers, plan=plan)


def hfft(
    x: Array,
    /,
    xp: Namespace,
    *,
    n: int | None = None,
    axis: int = -1,
    norm: _Norm = "backward",
) -> Array:
    res = xp.fft.hfft(x, n=n, axis=axis, norm=norm)
    if x.dtype in [xp.float32, xp.complex64]:
        return res.astype(xp.float32)
    return res


def hfft(a, n=None, axis=-1, norm=None, out=None):
    """
    Compute the FFT of a signal that has Hermitian symmetry, i.e., a real
    spectrum.

    Parameters
    ----------
    a : array_like
        The input array.
    n : int, optional
        Length of the transformed axis of the output. For `n` output
        points, ``n//2 + 1`` input points are necessary.  If the input is
        longer than this, it is cropped.  If it is shorter than this, it is
        padded with zeros.  If `n` is not given, it is taken to be ``2*(m-1)``
        where ``m`` is the length of the input along the axis specified by
        `axis`.
    axis : int, optional
        Axis over which to compute the FFT. If not given, the last
        axis is used.
    norm : {"backward", "ortho", "forward"}, optional
        Normalization mode (see `numpy.fft`). Default is "backward".
        Indicates which direction of the forward/backward pair of transforms
        is scaled and with what normalization factor.

        .. versionadded:: 1.20.0

            The "backward", "forward" values were added.

    out : ndarray, optional
        If provided, the result will be placed in this array. It should be
        of the appropriate shape and dtype.

        .. versionadded:: 2.0.0

    Returns
    -------
    out : ndarray
        The truncated or zero-padded input, transformed along the axis
        indicated by `axis`, or the last one if `axis` is not specified.
        The length of the transformed axis is `n`, or, if `n` is not given,
        ``2*m - 2`` where ``m`` is the length of the transformed axis of
        the input. To get an odd number of output points, `n` must be
        specified, for instance as ``2*m - 1`` in the typical case,

    Raises
    ------
    IndexError
        If `axis` is not a valid axis of `a`.

    See also
    --------
    rfft : Compute the one-dimensional FFT for real input.
    ihfft : The inverse of `hfft`.

    Notes
    -----
    `hfft`/`ihfft` are a pair analogous to `rfft`/`irfft`, but for the
    opposite case: here the signal has Hermitian symmetry in the time
    domain and is real in the frequency domain. So here it's `hfft` for
    which you must supply the length of the result if it is to be odd.

    * even: ``ihfft(hfft(a, 2*len(a) - 2)) == a``, within roundoff error,
    * odd: ``ihfft(hfft(a, 2*len(a) - 1)) == a``, within roundoff error.

    The correct interpretation of the hermitian input depends on the length of
    the original data, as given by `n`. This is because each input shape could
    correspond to either an odd or even length signal. By default, `hfft`
    assumes an even output length which puts the last entry at the Nyquist
    frequency; aliasing with its symmetric counterpart. By Hermitian symmetry,
    the value is thus treated as purely real. To avoid losing information, the
    shape of the full signal **must** be given.

    Examples
    --------
    >>> import numpy as np
    >>> signal = np.array([1, 2, 3, 4, 3, 2])
    >>> np.fft.fft(signal)
    array([15.+0.j,  -4.+0.j,   0.+0.j,  -1.-0.j,   0.+0.j,  -4.+0.j]) # may vary
    >>> np.fft.hfft(signal[:4]) # Input first half of signal
    array([15.,  -4.,   0.,  -1.,   0.,  -4.])
    >>> np.fft.hfft(signal, 6)  # Input entire signal and truncate
    array([15.,  -4.,   0.,  -1.,   0.,  -4.])


    >>> signal = np.array([[1, 1.j], [-1.j, 2]])
    >>> np.conj(signal.T) - signal   # check Hermitian symmetry
    array([[ 0.-0.j,  -0.+0.j], # may vary
           [ 0.+0.j,  0.-0.j]])
    >>> freq_spectrum = np.fft.hfft(signal)
    >>> freq_spectrum
    array([[ 1.,  1.],
           [ 2., -2.]])

    """
    a = asarray(a)
    if n is None:
        n = (a.shape[axis] - 1) * 2
    new_norm = _swap_direction(norm)
    output = irfft(conjugate(a), n, axis, norm=new_norm, out=out)
    return output


def hfft(a: ArrayLike, n: int | None = None,
         axis: int = -1, norm: str | None = None) -> Array:
  """Compute a 1-D FFT of an array whose spectrum has Hermitian symmetry.

  JAX implementation of :func:`numpy.fft.hfft`.

  Args:
    a: input array.
    n: optional, int. Specifies the dimension of the result along ``axis``. If
      not specified, ``n = 2*(m-1)``, where ``m`` is the dimension of ``a``
      along ``axis``.
    axis: optional, int, default=-1. Specifies the axis along which the transform
      is computed. If not specified, the transform is computed along axis -1.
    norm: optional, string. The normalization mode. "backward", "ortho" and "forward"
      are supported. Default is "backward".

  Returns:
    A real-valued array containing the one-dimensional discrete Fourier transform
    of ``a`` by exploiting its inherent Hermitian-symmetry, having a dimension of
    ``n`` along ``axis``.

  See also:
    - :func:`jax.numpy.fft.ihfft`: Computes a one-dimensional inverse FFT of an
      array whose spectrum has Hermitian symmetry.
    - :func:`jax.numpy.fft.fft`: Computes a one-dimensional discrete Fourier
      transform.
    - :func:`jax.numpy.fft.rfft`: Computes a one-dimensional discrete Fourier
      transform of a real-valued input.

  Examples:
    >>> x = jnp.array([[1, 3, 5, 7],
    ...                [2, 4, 6, 8]])
    >>> jnp.fft.hfft(x)
    Array([[24., -8.,  0., -2.,  0., -8.],
           [30., -8.,  0., -2.,  0., -8.]], dtype=float32)

    This value is equal to the real component of the discrete Fourier transform
    of the following array ``x1`` computed using ``jnp.fft.fft``.

    >>> x1 = jnp.array([[1, 3, 5, 7, 5, 3],
    ...                 [2, 4, 6, 8, 6, 4]])
    >>> jnp.fft.fft(x1)
    Array([[24.+0.j, -8.+0.j,  0.+0.j, -2.+0.j,  0.+0.j, -8.+0.j],
           [30.+0.j, -8.+0.j,  0.+0.j, -2.+0.j,  0.+0.j, -8.+0.j]],      dtype=complex64)
    >>> jnp.allclose(jnp.fft.hfft(x), jnp.fft.fft(x1))
    Array(True, dtype=bool)

    To obtain an odd-length output from ``jnp.fft.hfft``, ``n`` must be specified
    with an odd value, as the default behavior produces an even-length result
    along the specified ``axis``.

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   print(jnp.fft.hfft(x, n=5))
    [[17.   -5.24 -0.76 -0.76 -5.24]
     [22.   -5.24 -0.76 -0.76 -5.24]]

    When ``n=3`` and ``axis=0``, dimension of the transform along ``axis 0`` will
    be ``3`` and dimension along other axes will be same as that of input.

    >>> jnp.fft.hfft(x, n=3, axis=0)
    Array([[ 5., 11., 17., 23.],
           [-1., -1., -1., -1.],
           [-1., -1., -1., -1.]], dtype=float32)

    ``x`` can be reconstructed (but of complex datatype) using ``jnp.fft.ihfft``
    from the result of ``jnp.fft.hfft``, only when ``n`` is specified as ``2*(m-1)``
    if `m` is even or ``2*m-1`` if ``m`` is odd, where ``m`` is the dimension of
    input along ``axis``.

    >>> jnp.fft.ihfft(jnp.fft.hfft(x, 2*(x.shape[-1]-1)))
    Array([[1.+0.j, 3.+0.j, 5.+0.j, 7.+0.j],
           [2.+0.j, 4.+0.j, 6.+0.j, 8.+0.j]], dtype=complex64)
    >>> jnp.allclose(x, jnp.fft.ihfft(jnp.fft.hfft(x, 2*(x.shape[-1]-1))))
    Array(True, dtype=bool)

    For complex-valued inputs:

    >>> x2 = jnp.array([[1+2j, 3-4j, 5+6j],
    ...                 [2-3j, 4+5j, 6-7j]])
    >>> jnp.fft.hfft(x2)
    Array([[ 12., -12.,   0.,   4.],
           [ 16.,   6.,   0., -14.]], dtype=float32)
  """
  conj_a = ufuncs.conj(a)
  _axis_check_1d('hfft', axis)
  nn = (conj_a.shape[axis] - 1) * 2 if n is None else n
  return _fft_core_1d('hfft', lax_fft.FftType.IRFFT, conj_a, n=n, axis=axis,
                      norm=norm) * nn

