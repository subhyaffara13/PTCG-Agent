
def ifft(a: ArrayLike, n=None, axis=-1, norm=None):
    return torch.fft.ifft(a, n, dim=axis, norm=norm)


def ifft(
    input: TensorLikeType,
    n: int | None = None,
    dim: int = -1,
    norm: NormType = None,
) -> TensorLikeType:
    if input.dtype.is_complex:
        return _fft_c2c("ifft", input, n, dim, norm, forward=False)
    else:
        return _fft_r2c("ifft", input, n, dim, norm, forward=False, onesided=False)


def ifft(seq, dps=None):
    return _fourier_transform(seq, dps=dps, inverse=True)


def ifft(x, n=None, axis=-1, norm=None, overwrite_x=False, workers=None, *,
         plan=None):
    """
    Compute the 1-D inverse discrete Fourier Transform.

    This function computes the inverse of the 1-D *n*-point
    discrete Fourier transform computed by `fft`.  In other words,
    ``ifft(fft(x)) == x`` to within numerical accuracy.

    The input should be ordered in the same way as is returned by `fft`,
    i.e.,

    * ``x[0]`` should contain the zero frequency term,
    * ``x[1:n//2]`` should contain the positive-frequency terms,
    * ``x[n//2 + 1:]`` should contain the negative-frequency terms, in
      increasing order starting from the most negative frequency.

    For an even number of input points, ``x[n//2]`` represents the sum of
    the values at the positive and negative Nyquist frequencies, as the two
    are aliased together. See `fft` for details.

    Parameters
    ----------
    x : array_like
        Input array, can be complex.
    n : int, optional
        Length of the transformed axis of the output.
        If `n` is smaller than the length of the input, the input is cropped.
        If it is larger, the input is padded with zeros. If `n` is not given,
        the length of the input along the axis specified by `axis` is used.
        See notes about padding issues.
    axis : int, optional
        Axis over which to compute the inverse DFT. If not given, the last
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
    out : complex ndarray
        The truncated or zero-padded input, transformed along the axis
        indicated by `axis`, or the last one if `axis` is not specified.

    Raises
    ------
    IndexError
        If `axes` is larger than the last axis of `x`.

    See Also
    --------
    fft : The 1-D (forward) FFT, of which `ifft` is the inverse.
    ifft2 : The 2-D inverse FFT.
    ifftn : The N-D inverse FFT.

    Notes
    -----
    If the input parameter `n` is larger than the size of the input, the input
    is padded by appending zeros at the end. Even though this is the common
    approach, it might lead to surprising results. If a different padding is
    desired, it must be performed before calling `ifft`.

    If ``x`` is a 1-D array, then the `ifft` is equivalent to ::

        y[k] = np.sum(x * np.exp(2j * np.pi * k * np.arange(n)/n)) / len(x)

    As with `fft`, `ifft` has support for all floating point types and is
    optimized for real input.

    Examples
    --------
    >>> import scipy.fft
    >>> import numpy as np
    >>> scipy.fft.ifft([0, 4, 0, 0])
    array([ 1.+0.j,  0.+1.j, -1.+0.j,  0.-1.j]) # may vary

    Create and plot a band-limited signal with random phases:

    >>> import matplotlib.pyplot as plt
    >>> rng = np.random.default_rng()
    >>> t = np.arange(400)
    >>> n = np.zeros((400,), dtype=complex)
    >>> n[40:60] = np.exp(1j*rng.uniform(0, 2*np.pi, (20,)))
    >>> s = scipy.fft.ifft(n)
    >>> plt.plot(t, s.real, 'b-', t, s.imag, 'r--')
    [<matplotlib.lines.Line2D object at ...>, <matplotlib.lines.Line2D object at ...>]
    >>> plt.legend(('real', 'imaginary'))
    <matplotlib.legend.Legend object at ...>
    >>> plt.show()

    """
    return (Dispatchable(x, np.ndarray),)


def ifft(x, n=None, axis=-1, norm=None, overwrite_x=False, workers=None, *,
         plan=None):
    return _execute_1D('ifft', _duccfft.ifft, x, n=n, axis=axis, norm=norm,
                       overwrite_x=overwrite_x, workers=workers, plan=plan)


def ifft(x, n=None, axis=-1, overwrite_x=False):
    """
    Return discrete inverse Fourier transform of real or complex sequence.

    The returned complex array contains ``y(0), y(1),..., y(n-1)``, where

    ``y(j) = (x * exp(2*pi*sqrt(-1)*j*np.arange(n)/n)).mean()``.

    Parameters
    ----------
    x : array_like
        Transformed data to invert.
    n : int, optional
        Length of the inverse Fourier transform.  If ``n < x.shape[axis]``,
        `x` is truncated. If ``n > x.shape[axis]``, `x` is zero-padded.
        The default results in ``n = x.shape[axis]``.
    axis : int, optional
        Axis along which the ifft's are computed; the default is over the
        last axis (i.e., ``axis=-1``).
    overwrite_x : bool, optional
        If True, the contents of `x` can be destroyed; the default is False.

    Returns
    -------
    ifft : ndarray of floats
        The inverse discrete Fourier transform.

    See Also
    --------
    fft : Forward FFT

    Notes
    -----
    Both single and double precision routines are implemented. Half precision
    inputs will be converted to single precision. Non-floating-point inputs
    will be converted to double precision. Long-double precision inputs are
    not supported.

    This function is most efficient when `n` is a power of two, and least
    efficient when `n` is prime.

    If the data type of `x` is real, a "real IFFT" algorithm is automatically
    used, which roughly halves the computation time.

    Examples
    --------
    >>> from scipy.fftpack import fft, ifft
    >>> import numpy as np
    >>> x = np.arange(5)
    >>> np.allclose(ifft(fft(x)), x, atol=1e-15)  # within numerical accuracy.
    True

    """
    return _duccfft.ifft(x, n, axis, None, overwrite_x)


def ifft(
    x: Array,
    /,
    xp: Namespace,
    *,
    n: int | None = None,
    axis: int = -1,
    norm: _Norm = "backward",
) -> Array:
    res = xp.fft.ifft(x, n=n, axis=axis, norm=norm)
    if x.dtype in [xp.float32, xp.complex64]:
        return res.astype(xp.complex64)
    return res


def ifft(a, n=None, axis=-1, norm=None, out=None):
    """
    Compute the one-dimensional inverse discrete Fourier Transform.

    This function computes the inverse of the one-dimensional *n*-point
    discrete Fourier transform computed by `fft`.  In other words,
    ``ifft(fft(a)) == a`` to within numerical accuracy.
    For a general description of the algorithm and definitions,
    see `numpy.fft`.

    The input should be ordered in the same way as is returned by `fft`,
    i.e.,

    * ``a[0]`` should contain the zero frequency term,
    * ``a[1:n//2]`` should contain the positive-frequency terms,
    * ``a[n//2 + 1:]`` should contain the negative-frequency terms, in
      increasing order starting from the most negative frequency.

    For an even number of input points, ``A[n//2]`` represents the sum of
    the values at the positive and negative Nyquist frequencies, as the two
    are aliased together. See `numpy.fft` for details.

    Parameters
    ----------
    a : array_like
        Input array, can be complex.
    n : int, optional
        Length of the transformed axis of the output.
        If `n` is smaller than the length of the input, the input is cropped.
        If it is larger, the input is padded with zeros.  If `n` is not given,
        the length of the input along the axis specified by `axis` is used.
        See notes about padding issues.
    axis : int, optional
        Axis over which to compute the inverse DFT.  If not given, the last
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

    Raises
    ------
    IndexError
        If `axis` is not a valid axis of `a`.

    See Also
    --------
    numpy.fft : An introduction, with definitions and general explanations.
    fft : The one-dimensional (forward) FFT, of which `ifft` is the inverse
    ifft2 : The two-dimensional inverse FFT.
    ifftn : The n-dimensional inverse FFT.

    Notes
    -----
    If the input parameter `n` is larger than the size of the input, the input
    is padded by appending zeros at the end.  Even though this is the common
    approach, it might lead to surprising results.  If a different padding is
    desired, it must be performed before calling `ifft`.

    Examples
    --------
    >>> import numpy as np
    >>> np.fft.ifft([0, 4, 0, 0])
    array([ 1.+0.j,  0.+1.j, -1.+0.j,  0.-1.j]) # may vary

    Create and plot a band-limited signal with random phases:

    >>> import matplotlib.pyplot as plt
    >>> t = np.arange(400)
    >>> n = np.zeros((400,), dtype=np.complex128)
    >>> n[40:60] = np.exp(1j*np.random.uniform(0, 2*np.pi, (20,)))
    >>> s = np.fft.ifft(n)
    >>> plt.plot(t, s.real, label='real')
    [<matplotlib.lines.Line2D object at ...>]
    >>> plt.plot(t, s.imag, '--', label='imaginary')
    [<matplotlib.lines.Line2D object at ...>]
    >>> plt.legend()
    <matplotlib.legend.Legend object at ...>
    >>> plt.show()

    """
    a = asarray(a)
    if n is None:
        n = a.shape[axis]
    output = _raw_fft(a, n, axis, False, False, norm, out=out)
    return output


def ifft(a: ArrayLike, n: int | None = None,
         axis: int = -1, norm: str | None = None) -> Array:
  r"""Compute a one-dimensional inverse discrete Fourier transform.

  JAX implementation of :func:`numpy.fft.ifft`.

  Args:
    a: input array
    n: int. Specifies the dimension of the result along ``axis``. If not specified,
      it will default to the dimension of ``a`` along ``axis``.
    axis: int, default=-1. Specifies the axis along which the transform is computed.
      If not specified, the transform is computed along axis -1.
    norm: string. The normalization mode. "backward", "ortho" and "forward" are
      supported.

  Returns:
    An array containing the one-dimensional discrete Fourier transform of ``a``.

  See also:
    - :func:`jax.numpy.fft.fft`: Computes a one-dimensional discrete Fourier
      transform.
    - :func:`jax.numpy.fft.fftn`: Computes a multidimensional discrete Fourier
      transform.
    - :func:`jax.numpy.fft.ifftn`: Computes a multidimensional inverse of discrete
      Fourier transform.

  Examples:
    ``jnp.fft.ifft`` computes the transform along ``axis -1`` by default.

    >>> x = jnp.array([[3, 1, 4, 6],
    ...                [2, 5, 7, 1]])
    >>> jnp.fft.ifft(x)
    Array([[ 3.5 +0.j  , -0.25-1.25j,  0.  +0.j  , -0.25+1.25j],
          [ 3.75+0.j  , -1.25+1.j  ,  0.75+0.j  , -1.25-1.j  ]],      dtype=complex64)

    When ``n=5``, dimension of the transform along axis -1 will be ``5`` and
    dimension along other axes will be the same as that of input.

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   print(jnp.fft.ifft(x, n=5))
    [[ 2.8 +0.j   -0.96-0.04j  1.06+0.5j   1.06-0.5j  -0.96+0.04j]
     [ 3.  +0.j   -0.59+1.66j  0.09-0.55j  0.09+0.55j -0.59-1.66j]]

    When ``n=3`` and ``axis=0``, dimension of the transform along ``axis 0`` will
    be ``3`` and dimension along other axes will be same as that of input.

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   print(jnp.fft.ifft(x, n=3, axis=0))
    [[ 1.67+0.j    2.  +0.j    3.67+0.j    2.33+0.j  ]
     [ 0.67+0.58j -0.5 +1.44j  0.17+2.02j  1.83+0.29j]
     [ 0.67-0.58j -0.5 -1.44j  0.17-2.02j  1.83-0.29j]]
  """
  return _fft_core_1d('ifft', lax_fft.FftType.IFFT, a, n=n, axis=axis,
                      norm=norm)

