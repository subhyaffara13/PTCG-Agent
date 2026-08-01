
def rfft(a: ArrayLike, n=None, axis=-1, norm=None):
    return torch.fft.rfft(a, n, dim=axis, norm=norm)


def rfft(
    input: TensorLikeType,
    n: int | None = None,
    dim: int = -1,
    norm: NormType = None,
) -> TensorLikeType:
    return _fft_r2c("rfft", input, n, dim, norm, forward=True, onesided=True)


def rfft(x, n=None, axis=-1, norm=None, overwrite_x=False, workers=None, *,
         plan=None):
    """
    Compute the 1-D discrete Fourier Transform for real input.

    This function computes the 1-D *n*-point discrete Fourier
    Transform (DFT) of a real-valued array by means of an efficient algorithm
    called the Fast Fourier Transform (FFT).

    Parameters
    ----------
    x : array_like
        Input array
    n : int, optional
        Number of points along transformation axis in the input to use.
        If `n` is smaller than the length of the input, the input is cropped.
        If it is larger, the input is padded with zeros. If `n` is not given,
        the length of the input along the axis specified by `axis` is used.
    axis : int, optional
        Axis over which to compute the FFT. If not given, the last axis is
        used.
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
    out : complex ndarray
        The truncated or zero-padded input, transformed along the axis
        indicated by `axis`, or the last one if `axis` is not specified.
        If `n` is even, the length of the transformed axis is ``(n/2)+1``.
        If `n` is odd, the length is ``(n+1)/2``.

    Raises
    ------
    IndexError
        If `axis` is larger than the last axis of `a`.

    See Also
    --------
    irfft : The inverse of `rfft`.
    fft : The 1-D FFT of general (complex) input.
    fftn : The N-D FFT.
    rfft2 : The 2-D FFT of real input.
    rfftn : The N-D FFT of real input.

    Notes
    -----
    When the DFT is computed for purely real input, the output is
    Hermitian-symmetric, i.e., the negative frequency terms are just the complex
    conjugates of the corresponding positive-frequency terms, and the
    negative-frequency terms are therefore redundant. This function does not
    compute the negative frequency terms, and the length of the transformed
    axis of the output is therefore ``n//2 + 1``.

    When ``X = rfft(x)`` and fs is the sampling frequency, ``X[0]`` contains
    the zero-frequency term 0*fs, which is real due to Hermitian symmetry.

    If `n` is even, ``A[-1]`` contains the term representing both positive
    and negative Nyquist frequency (+fs/2 and -fs/2), and must also be purely
    real. If `n` is odd, there is no term at fs/2; ``A[-1]`` contains
    the largest positive frequency (fs/2*(n-1)/n), and is complex in the
    general case.

    If the input `a` contains an imaginary part, it is silently discarded.

    Examples
    --------
    >>> import scipy.fft
    >>> scipy.fft.fft([0, 1, 0, 0])
    array([ 1.+0.j,  0.-1.j, -1.+0.j,  0.+1.j]) # may vary
    >>> scipy.fft.rfft([0, 1, 0, 0])
    array([ 1.+0.j,  0.-1.j, -1.+0.j]) # may vary

    Notice how the final element of the `fft` output is the complex conjugate
    of the second element, for real input. For `rfft`, this symmetry is
    exploited to compute only the non-negative frequency terms.

    """
    return (Dispatchable(x, np.ndarray),)


def rfft(x, n=None, axis=-1, norm=None,
         overwrite_x=False, workers=None, *, plan=None):
    return _execute_1D('rfft', _duccfft.rfft, x, n=n, axis=axis, norm=norm,
                       overwrite_x=overwrite_x, workers=workers, plan=plan)


def rfft(x, n=None, axis=-1, overwrite_x=False):
    """
    Discrete Fourier transform of a real sequence.

    Parameters
    ----------
    x : array_like, real-valued
        The data to transform.
    n : int, optional
        Defines the length of the Fourier transform. If `n` is not specified
        (the default) then ``n = x.shape[axis]``. If ``n < x.shape[axis]``,
        `x` is truncated, if ``n > x.shape[axis]``, `x` is zero-padded.
    axis : int, optional
        The axis along which the transform is applied. The default is the
        last axis.
    overwrite_x : bool, optional
        If set to true, the contents of `x` can be overwritten. Default is
        False.

    Returns
    -------
    z : real ndarray
        The returned real array contains::

          [y(0),Re(y(1)),Im(y(1)),...,Re(y(n/2))]              if n is even
          [y(0),Re(y(1)),Im(y(1)),...,Re(y(n/2)),Im(y(n/2))]   if n is odd

        where::

          y(j) = sum[k=0..n-1] x[k] * exp(-sqrt(-1)*j*k*2*pi/n)
          j = 0..n-1

    See Also
    --------
    fft, irfft, scipy.fft.rfft

    Notes
    -----
    Within numerical accuracy, ``y == rfft(irfft(y))``.

    Both single and double precision routines are implemented. Half precision
    inputs will be converted to single precision. Non-floating-point inputs
    will be converted to double precision. Long-double precision inputs are
    not supported.

    To get an output with a complex datatype, consider using the newer
    function `scipy.fft.rfft`.

    Examples
    --------
    >>> from scipy.fftpack import fft, rfft
    >>> a = [9, -9, 1, 3]
    >>> fft(a)
    array([  4. +0.j,   8.+12.j,  16. +0.j,   8.-12.j])
    >>> rfft(a)
    array([  4.,   8.,  12.,  16.])

    """
    return _duccfft.rfft_fftpack(x, n, axis, None, overwrite_x)


def rfft(
    x: Array,
    /,
    xp: Namespace,
    *,
    n: int | None = None,
    axis: int = -1,
    norm: _Norm = "backward",
) -> Array:
    res = xp.fft.rfft(x, n=n, axis=axis, norm=norm)
    if x.dtype == xp.float32:
        return res.astype(xp.complex64)
    return res


def rfft(a, n=None, axis=-1, norm=None, out=None):
    """
    Compute the one-dimensional discrete Fourier Transform for real input.

    This function computes the one-dimensional *n*-point discrete Fourier
    Transform (DFT) of a real-valued array by means of an efficient algorithm
    called the Fast Fourier Transform (FFT).

    Parameters
    ----------
    a : array_like
        Input array
    n : int, optional
        Number of points along transformation axis in the input to use.
        If `n` is smaller than the length of the input, the input is cropped.
        If it is larger, the input is padded with zeros. If `n` is not given,
        the length of the input along the axis specified by `axis` is used.
    axis : int, optional
        Axis over which to compute the FFT. If not given, the last axis is
        used.
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
        If `n` is even, the length of the transformed axis is ``(n/2)+1``.
        If `n` is odd, the length is ``(n+1)/2``.

    Raises
    ------
    IndexError
        If `axis` is not a valid axis of `a`.

    See Also
    --------
    numpy.fft : For definition of the DFT and conventions used.
    irfft : The inverse of `rfft`.
    fft : The one-dimensional FFT of general (complex) input.
    fftn : The *n*-dimensional FFT.
    rfftn : The *n*-dimensional FFT of real input.

    Notes
    -----
    When the DFT is computed for purely real input, the output is
    Hermitian-symmetric, i.e. the negative frequency terms are just the complex
    conjugates of the corresponding positive-frequency terms, and the
    negative-frequency terms are therefore redundant.  This function does not
    compute the negative frequency terms, and the length of the transformed
    axis of the output is therefore ``n//2 + 1``.

    When ``A = rfft(a)`` and fs is the sampling frequency, ``A[0]`` contains
    the zero-frequency term 0*fs, which is real due to Hermitian symmetry.

    If `n` is even, ``A[-1]`` contains the term representing both positive
    and negative Nyquist frequency (+fs/2 and -fs/2), and must also be purely
    real. If `n` is odd, there is no term at fs/2; ``A[-1]`` contains
    the largest positive frequency (fs/2*(n-1)/n), and is complex in the
    general case.

    If the input `a` contains an imaginary part, it is silently discarded.

    Examples
    --------
    >>> import numpy as np
    >>> np.fft.fft([0, 1, 0, 0])
    array([ 1.+0.j,  0.-1.j, -1.+0.j,  0.+1.j]) # may vary
    >>> np.fft.rfft([0, 1, 0, 0])
    array([ 1.+0.j,  0.-1.j, -1.+0.j]) # may vary

    Notice how the final element of the `fft` output is the complex conjugate
    of the second element, for real input. For `rfft`, this symmetry is
    exploited to compute only the non-negative frequency terms.

    """
    a = asarray(a)
    if n is None:
        n = a.shape[axis]
    output = _raw_fft(a, n, axis, True, True, norm, out=out)
    return output


def rfft(a: ArrayLike, n: int | None = None,
         axis: int = -1, norm: str | None = None) -> Array:
  r"""Compute a one-dimensional discrete Fourier transform of a real-valued array.

  JAX implementation of :func:`numpy.fft.rfft`.

  Args:
    a: real-valued input array.
    n: int. Specifies the effective dimension of the input along ``axis``. If not
      specified, it will default to the dimension of input along ``axis``.
    axis: int, default=-1. Specifies the axis along which the transform is computed.
      If not specified, the transform is computed along axis -1.
    norm: string. The normalization mode. "backward", "ortho" and "forward" are
      supported.

  Returns:
    An array containing the one-dimensional discrete Fourier transform of ``a``.
    The dimension of the array along ``axis`` is ``(n/2)+1``, if ``n`` is even and
    ``(n+1)/2``, if ``n`` is odd.

  See also:
    - :func:`jax.numpy.fft.fft`: Computes a one-dimensional discrete Fourier
      transform.
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
    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   jnp.fft.rfft(x)
    Array([[ 9.+0.j  , -3.+1.73j],
           [12.+0.j  , -3.+1.73j]], dtype=complex64)

    When ``n=5``, dimension of the transform along axis -1 will be ``(5+1)/2 =3``
    and dimension along other axes will be the same as that of input.

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   jnp.fft.rfft(x, n=5)
    Array([[ 9.  +0.j  , -2.12-5.79j,  0.12+2.99j],
           [12.  +0.j  , -1.62-7.33j,  0.62+3.36j]], dtype=complex64)

    When ``n=4`` and ``axis=0``, dimension of the transform along ``axis 0`` will
    be ``(4/2)+1 =3`` and dimension along other axes will be same as that of input.

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   jnp.fft.rfft(x, n=4, axis=0)
    Array([[ 3.+0.j,  7.+0.j, 11.+0.j],
           [ 1.-2.j,  3.-4.j,  5.-6.j],
           [-1.+0.j, -1.+0.j, -1.+0.j]], dtype=complex64)
  """
  return _fft_core_1d('rfft', lax_fft.FftType.RFFT, a, n=n, axis=axis,
                      norm=norm)

