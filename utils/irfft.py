
def irfft(a: ArrayLike, n=None, axis=-1, norm=None):
    return torch.fft.irfft(a, n, dim=axis, norm=norm)


def irfft(
    input: TensorLikeType,
    n: int | None = None,
    dim: int = -1,
    norm: NormType = None,
) -> TensorLikeType:
    return _fft_c2r("irfft", input, n, dim, norm, forward=False)


def irfft(x, n=None, axis=-1, norm=None, overwrite_x=False, workers=None, *,
          plan=None):
    """
    Computes the inverse of `rfft`.

    This function computes the inverse of the 1-D *n*-point
    discrete Fourier Transform of real input computed by `rfft`.
    In other words, ``irfft(rfft(x), len(x)) == x`` to within numerical
    accuracy. (See Notes below for why ``len(a)`` is necessary here.)

    The input is expected to be in the form returned by `rfft`, i.e., the
    real zero-frequency term followed by the complex positive frequency terms
    in order of increasing frequency. Since the discrete Fourier Transform of
    real input is Hermitian-symmetric, the negative frequency terms are taken
    to be the complex conjugates of the corresponding positive frequency terms.

    Parameters
    ----------
    x : array_like
        The input array.
    n : int, optional
        Length of the transformed axis of the output.
        For `n` output points, ``n//2+1`` input points are necessary. If the
        input is longer than this, it is cropped. If it is shorter than this,
        it is padded with zeros. If `n` is not given, it is taken to be
        ``2*(m-1)``, where ``m`` is the length of the input along the axis
        specified by `axis`.
    axis : int, optional
        Axis over which to compute the inverse FFT. If not given, the last
        axis is used.
    norm : {"backward", "ortho", "forward"}, optional
        Normalization mode (see `fft`). Default is "backward".
    overwrite_x : bool, optional
        If True, the contents of `x` can be destroyed; the default is False.
        See :func:`fft` for more details.
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
        ``2*(m-1)`` where ``m`` is the length of the transformed axis of the
        input. To get an odd number of output points, `n` must be specified.

    Raises
    ------
    IndexError
        If `axis` is larger than the last axis of `x`.

    See Also
    --------
    rfft : The 1-D FFT of real input, of which `irfft` is inverse.
    fft : The 1-D FFT.
    irfft2 : The inverse of the 2-D FFT of real input.
    irfftn : The inverse of the N-D FFT of real input.

    Notes
    -----
    Returns the real valued `n`-point inverse discrete Fourier transform
    of `x`, where `x` contains the non-negative frequency terms of a
    Hermitian-symmetric sequence. `n` is the length of the result, not the
    input.

    If you specify an `n` such that `a` must be zero-padded or truncated, the
    extra/removed values will be added/removed at high frequencies. One can
    thus resample a series to `m` points via Fourier interpolation by:
    ``a_resamp = irfft(rfft(a), m)``.

    The default value of `n` assumes an even output length. By the Hermitian
    symmetry, the last imaginary component must be 0 and so is ignored. To
    avoid losing information, the correct length of the real input *must* be
    given.

    Examples
    --------
    >>> import scipy.fft
    >>> scipy.fft.ifft([1, -1j, -1, 1j])
    array([0.+0.j,  1.+0.j,  0.+0.j,  0.+0.j]) # may vary
    >>> scipy.fft.irfft([1, -1j, -1])
    array([0.,  1.,  0.,  0.])

    Notice how the last term in the input to the ordinary `ifft` is the
    complex conjugate of the second term, and the output has zero imaginary
    part everywhere. When calling `irfft`, the negative frequencies are not
    specified, and the output array is purely real.

    """
    return (Dispatchable(x, np.ndarray),)


def irfft(x, n=None, axis=-1, norm=None,
          overwrite_x=False, workers=None, *, plan=None):
    return _execute_1D('irfft', _duccfft.irfft, x, n=n, axis=axis, norm=norm,
                       overwrite_x=overwrite_x, workers=workers, plan=plan)


def irfft(x, n=None, axis=-1, overwrite_x=False):
    """
    Return inverse discrete Fourier transform of real sequence x.

    The contents of `x` are interpreted as the output of the `rfft`
    function.

    Parameters
    ----------
    x : array_like
        Transformed data to invert.
    n : int, optional
        Length of the inverse Fourier transform.
        If n < x.shape[axis], x is truncated.
        If n > x.shape[axis], x is zero-padded.
        The default results in n = x.shape[axis].
    axis : int, optional
        Axis along which the ifft's are computed; the default is over
        the last axis (i.e., axis=-1).
    overwrite_x : bool, optional
        If True, the contents of `x` can be destroyed; the default is False.

    Returns
    -------
    irfft : ndarray of floats
        The inverse discrete Fourier transform.

    See Also
    --------
    rfft, ifft, scipy.fft.irfft

    Notes
    -----
    The returned real array contains::

        [y(0),y(1),...,y(n-1)]

    where for n is even::

        y(j) = 1/n (sum[k=1..n/2-1] (x[2*k-1]+sqrt(-1)*x[2*k])
                                     * exp(sqrt(-1)*j*k* 2*pi/n)
                    + c.c. + x[0] + (-1)**(j) x[n-1])

    and for n is odd::

        y(j) = 1/n (sum[k=1..(n-1)/2] (x[2*k-1]+sqrt(-1)*x[2*k])
                                     * exp(sqrt(-1)*j*k* 2*pi/n)
                    + c.c. + x[0])

    c.c. denotes complex conjugate of preceding expression.

    For details on input parameters, see `rfft`.

    To process (conjugate-symmetric) frequency-domain data with a complex
    datatype, consider using the newer function `scipy.fft.irfft`.

    Examples
    --------
    >>> from scipy.fftpack import rfft, irfft
    >>> a = [1.0, 2.0, 3.0, 4.0, 5.0]
    >>> irfft(a)
    array([ 2.6       , -3.16405192,  1.24398433, -1.14955713,  1.46962473])
    >>> irfft(rfft(a))
    array([1., 2., 3., 4., 5.])

    """
    return _duccfft.irfft_fftpack(x, n, axis, None, overwrite_x)


def irfft(
    x: Array,
    /,
    xp: Namespace,
    *,
    n: int | None = None,
    axis: int = -1,
    norm: _Norm = "backward",
) -> Array:
    res = xp.fft.irfft(x, n=n, axis=axis, norm=norm)
    if x.dtype == xp.complex64:
        return res.astype(xp.float32)
    return res


def irfft(a, n=None, axis=-1, norm=None, out=None):
    """
    Computes the inverse of `rfft`.

    This function computes the inverse of the one-dimensional *n*-point
    discrete Fourier Transform of real input computed by `rfft`.
    In other words, ``irfft(rfft(a), len(a)) == a`` to within numerical
    accuracy. (See Notes below for why ``len(a)`` is necessary here.)

    The input is expected to be in the form returned by `rfft`, i.e. the
    real zero-frequency term followed by the complex positive frequency terms
    in order of increasing frequency.  Since the discrete Fourier Transform of
    real input is Hermitian-symmetric, the negative frequency terms are taken
    to be the complex conjugates of the corresponding positive frequency terms.

    Parameters
    ----------
    a : array_like
        The input array.
    n : int, optional
        Length of the transformed axis of the output.
        For `n` output points, ``n//2+1`` input points are necessary.  If the
        input is longer than this, it is cropped.  If it is shorter than this,
        it is padded with zeros.  If `n` is not given, it is taken to be
        ``2*(m-1)`` where ``m`` is the length of the input along the axis
        specified by `axis`.
    axis : int, optional
        Axis over which to compute the inverse FFT. If not given, the last
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
        ``2*(m-1)`` where ``m`` is the length of the transformed axis of the
        input. To get an odd number of output points, `n` must be specified.

    Raises
    ------
    IndexError
        If `axis` is not a valid axis of `a`.

    See Also
    --------
    numpy.fft : For definition of the DFT and conventions used.
    rfft : The one-dimensional FFT of real input, of which `irfft` is inverse.
    fft : The one-dimensional FFT.
    irfft2 : The inverse of the two-dimensional FFT of real input.
    irfftn : The inverse of the *n*-dimensional FFT of real input.

    Notes
    -----
    Returns the real valued `n`-point inverse discrete Fourier transform
    of `a`, where `a` contains the non-negative frequency terms of a
    Hermitian-symmetric sequence. `n` is the length of the result, not the
    input.

    If you specify an `n` such that `a` must be zero-padded or truncated, the
    extra/removed values will be added/removed at high frequencies. One can
    thus resample a series to `m` points via Fourier interpolation by:
    ``a_resamp = irfft(rfft(a), m)``.

    The correct interpretation of the hermitian input depends on the length of
    the original data, as given by `n`. This is because each input shape could
    correspond to either an odd or even length signal. By default, `irfft`
    assumes an even output length which puts the last entry at the Nyquist
    frequency; aliasing with its symmetric counterpart. By Hermitian symmetry,
    the value is thus treated as purely real. To avoid losing information, the
    correct length of the real input **must** be given.

    Examples
    --------
    >>> import numpy as np
    >>> np.fft.ifft([1, -1j, -1, 1j])
    array([0.+0.j,  1.+0.j,  0.+0.j,  0.+0.j]) # may vary
    >>> np.fft.irfft([1, -1j, -1])
    array([0.,  1.,  0.,  0.])

    Notice how the last term in the input to the ordinary `ifft` is the
    complex conjugate of the second term, and the output has zero imaginary
    part everywhere.  When calling `irfft`, the negative frequencies are not
    specified, and the output array is purely real.

    """
    a = asarray(a)
    if n is None:
        n = (a.shape[axis] - 1) * 2
    output = _raw_fft(a, n, axis, True, False, norm, out=out)
    return output


def irfft(a: ArrayLike, n: int | None = None,
          axis: int = -1, norm: str | None = None) -> Array:
  """Compute a real-valued one-dimensional inverse discrete Fourier transform.

  JAX implementation of :func:`numpy.fft.irfft`.

  Args:
    a: input array.
    n: int. Specifies the dimension of the result along ``axis``. If not specified,
      ``n = 2*(m-1)``, where ``m`` is the dimension of ``a`` along ``axis``.
    axis: int, default=-1. Specifies the axis along which the transform is computed.
      If not specified, the transform is computed along axis -1.
    norm: string. The normalization mode. "backward", "ortho" and "forward" are
      supported.

  Returns:
    A real-valued array containing the one-dimensional inverse discrete Fourier
    transform of ``a``, with a dimension of ``n`` along ``axis``.

  See also:
    - :func:`jax.numpy.fft.ifft`: Computes a one-dimensional inverse discrete
      Fourier transform.
    - :func:`jax.numpy.fft.irfft`: Computes a one-dimensional inverse discrete
      Fourier transform for real input.
    - :func:`jax.numpy.fft.rfftn`: Computes a multidimensional discrete Fourier
      transform for real input.
    - :func:`jax.numpy.fft.irfftn`: Computes a multidimensional inverse discrete
      Fourier transform for real input.

  Examples:
    ``jnp.fft.rfft`` computes the transform along ``axis -1`` by default.

    >>> x = jnp.array([[1, 3, 5],
    ...                [2, 4, 6]])
    >>> jnp.fft.irfft(x)
    Array([[ 3., -1.,  0., -1.],
           [ 4., -1.,  0., -1.]], dtype=float32)

    When ``n=3``, dimension of the transform along axis -1 will be ``3`` and
    dimension along other axes will be the same as that of input.

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   jnp.fft.irfft(x, n=3)
    Array([[ 2.33, -0.67, -0.67],
           [ 3.33, -0.67, -0.67]], dtype=float32)

    When ``n=4`` and ``axis=0``, dimension of the transform along ``axis 0`` will
    be ``4`` and dimension along other axes will be same as that of input.

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   jnp.fft.irfft(x, n=4, axis=0)
    Array([[ 1.25,  2.75,  4.25],
           [ 0.25,  0.75,  1.25],
           [-0.75, -1.25, -1.75],
           [ 0.25,  0.75,  1.25]], dtype=float32)
  """
  return _fft_core_1d('irfft', lax_fft.FftType.IRFFT, a, n=n, axis=axis,
                      norm=norm)

