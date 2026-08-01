
def fft(a: ArrayLike, n=None, axis=-1, norm=None):
    return torch.fft.fft(a, n, dim=axis, norm=norm)


def fft(
    input: TensorLikeType,
    n: int | None = None,
    dim: int = -1,
    norm: NormType = None,
) -> TensorLikeType:
    if input.dtype.is_complex:
        return _fft_c2c("fft", input, n, dim, norm, forward=True)
    else:
        return _fft_r2c("fft", input, n, dim, norm, forward=True, onesided=False)


def fft(seq, dps=None):
    r"""
    Performs the Discrete Fourier Transform (**DFT**) in the complex domain.

    The sequence is automatically padded to the right with zeros, as the
    *radix-2 FFT* requires the number of sample points to be a power of 2.

    This method should be used with default arguments only for short sequences
    as the complexity of expressions increases with the size of the sequence.

    Parameters
    ==========

    seq : iterable
        The sequence on which **DFT** is to be applied.
    dps : Integer
        Specifies the number of decimal digits for precision.

    Examples
    ========

    >>> from sympy import fft, ifft

    >>> fft([1, 2, 3, 4])
    [10, -2 - 2*I, -2, -2 + 2*I]
    >>> ifft(_)
    [1, 2, 3, 4]

    >>> ifft([1, 2, 3, 4])
    [5/2, -1/2 + I/2, -1/2, -1/2 - I/2]
    >>> fft(_)
    [1, 2, 3, 4]

    >>> ifft([1, 7, 3, 4], dps=15)
    [3.75, -0.5 - 0.75*I, -1.75, -0.5 + 0.75*I]
    >>> fft(_)
    [1.0, 7.0, 3.0, 4.0]

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Cooley%E2%80%93Tukey_FFT_algorithm
    .. [2] https://mathworld.wolfram.com/FastFourierTransform.html

    """

    return _fourier_transform(seq, dps=dps)


def fft(x, n=None, axis=-1, norm=None, overwrite_x=False, workers=None, *,
        plan=None):
    """
    Compute the 1-D discrete Fourier Transform.

    This function computes the 1-D *n*-point discrete Fourier
    Transform (DFT) with the efficient Fast Fourier Transform (FFT)
    algorithm [1]_.

    Parameters
    ----------
    x : array_like
        Input array, can be complex.
    n : int, optional
        Length of the transformed axis of the output.
        If `n` is smaller than the length of the input, the input is cropped.
        If it is larger, the input is padded with zeros. If `n` is not given,
        the length of the input along the axis specified by `axis` is used.
    axis : int, optional
        Axis over which to compute the FFT. If not given, the last axis is
        used.
    norm : {"backward", "ortho", "forward"}, optional
        Normalization mode. Default is "backward", meaning no normalization on
        the forward transforms and scaling by ``1/n`` on the `ifft`.
        "forward" instead applies the ``1/n`` factor on the forward transform.
        For ``norm="ortho"``, both directions are scaled by ``1/sqrt(n)``.

        .. versionadded:: 1.6.0
           ``norm={"forward", "backward"}`` options were added

    overwrite_x : bool, optional
        If True, the contents of `x` can be destroyed; the default is False.
        See the notes below for more details.
    workers : int, optional
        Maximum number of workers to use for parallel computation. If negative,
        the value wraps around from ``os.cpu_count()``. See below for more
        details.
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
        if `axes` is larger than the last axis of `x`.

    See Also
    --------
    ifft : The inverse of `fft`.
    fft2 : The 2-D FFT.
    fftn : The N-D FFT.
    rfftn : The N-D FFT of real input.
    fftfreq : Frequency bins for given FFT parameters.
    next_fast_len : Size to pad input to for most efficient transforms

    Notes
    -----
    FFT (Fast Fourier Transform) refers to a way the discrete Fourier Transform
    (DFT) can be calculated efficiently, by using symmetries in the calculated
    terms. The symmetry is highest when `n` is a power of 2, and the transform
    is therefore most efficient for these sizes. For poorly factorizable sizes,
    `scipy.fft` uses Bluestein's algorithm [2]_ and so is never worse than
    O(`n` log `n`). Further performance improvements may be seen by zero-padding
    the input using `next_fast_len`.

    If ``x`` is a 1d array, then the `fft` is equivalent to ::

        y[k] = np.sum(x * np.exp(-2j * np.pi * k * np.arange(n)/n))

    The frequency term ``f=k/n`` is found at ``y[k]``. At ``y[n/2]`` we reach
    the Nyquist frequency and wrap around to the negative-frequency terms. So,
    for an 8-point transform, the frequencies of the result are
    [0, 1, 2, 3, -4, -3, -2, -1]. To rearrange the fft output so that the
    zero-frequency component is centered, like [-4, -3, -2, -1, 0, 1, 2, 3],
    use `fftshift`.

    Transforms can be done in single, double, or extended precision (long
    double) floating point. Half precision inputs will be converted to single
    precision and non-floating-point inputs will be converted to double
    precision.

    If the data type of ``x`` is real, a "real FFT" algorithm is automatically
    used, which roughly halves the computation time. To increase efficiency
    a little further, use `rfft`, which does the same calculation, but only
    outputs half of the symmetrical spectrum. If the data are both real and
    symmetrical, the `dct` can again double the efficiency, by generating
    half of the spectrum from half of the signal.

    When ``overwrite_x=True`` is specified, the memory referenced by ``x`` may
    be used by the implementation in any way. This may include reusing the
    memory for the result, but this is in no way guaranteed. You should not
    rely on the contents of ``x`` after the transform as this may change in
    future without warning.

    The ``workers`` argument specifies the maximum number of parallel jobs to
    split the FFT computation into. This will execute independent 1-D
    FFTs within ``x``. So, ``x`` must be at least 2-D and the
    non-transformed axes must be large enough to split into chunks. If ``x`` is
    too small, fewer jobs may be used than requested.

    References
    ----------
    .. [1] Cooley, James W., and John W. Tukey, 1965, "An algorithm for the
           machine calculation of complex Fourier series," *Math. Comput.*
           19: 297-301.
    .. [2] Bluestein, L., 1970, "A linear filtering approach to the
           computation of discrete Fourier transform". *IEEE Transactions on
           Audio and Electroacoustics.* 18 (4): 451-455.

    Examples
    --------
    >>> import scipy.fft
    >>> import numpy as np
    >>> scipy.fft.fft(np.exp(2j * np.pi * np.arange(8) / 8))
    array([-2.33486982e-16+1.14423775e-17j,  8.00000000e+00-1.25557246e-15j,
            2.33486982e-16+2.33486982e-16j,  0.00000000e+00+1.22464680e-16j,
           -1.14423775e-17+2.33486982e-16j,  0.00000000e+00+5.20784380e-16j,
            1.14423775e-17+1.14423775e-17j,  0.00000000e+00+1.22464680e-16j])

    In this example, real input has an FFT which is Hermitian, i.e., symmetric
    in the real part and anti-symmetric in the imaginary part:

    >>> from scipy.fft import fft, fftfreq, fftshift
    >>> import matplotlib.pyplot as plt
    >>> t = np.arange(256)
    >>> sp = fftshift(fft(np.sin(t)))
    >>> freq = fftshift(fftfreq(t.shape[-1]))
    >>> plt.plot(freq, sp.real, freq, sp.imag)
    [<matplotlib.lines.Line2D object at 0x...>,
     <matplotlib.lines.Line2D object at 0x...>]
    >>> plt.show()

    """
    return (Dispatchable(x, np.ndarray),)


def fft(x, n=None, axis=-1, norm=None,
        overwrite_x=False, workers=None, *, plan=None):
    return _execute_1D('fft', _duccfft.fft, x, n=n, axis=axis, norm=norm,
                       overwrite_x=overwrite_x, workers=workers, plan=plan)


def fft(x, n=None, axis=-1, overwrite_x=False):
    """
    Return discrete Fourier transform of real or complex sequence.

    The returned complex array contains ``y(0), y(1),..., y(n-1)``, where

    ``y(j) = (x * exp(-2*pi*sqrt(-1)*j*np.arange(n)/n)).sum()``.

    Parameters
    ----------
    x : array_like
        Array to Fourier transform.
    n : int, optional
        Length of the Fourier transform. If ``n < x.shape[axis]``, `x` is
        truncated. If ``n > x.shape[axis]``, `x` is zero-padded. The
        default results in ``n = x.shape[axis]``.
    axis : int, optional
        Axis along which the fft's are computed; the default is over the
        last axis (i.e., ``axis=-1``).
    overwrite_x : bool, optional
        If True, the contents of `x` can be destroyed; the default is False.

    Returns
    -------
    z : complex ndarray
        with the elements::

            [y(0),y(1),..,y(n/2),y(1-n/2),...,y(-1)]        if n is even
            [y(0),y(1),..,y((n-1)/2),y(-(n-1)/2),...,y(-1)]  if n is odd

        where::

            y(j) = sum[k=0..n-1] x[k] * exp(-sqrt(-1)*j*k* 2*pi/n), j = 0..n-1

    See Also
    --------
    ifft : Inverse FFT
    rfft : FFT of a real sequence

    Notes
    -----
    The packing of the result is "standard": If ``A = fft(a, n)``, then
    ``A[0]`` contains the zero-frequency term, ``A[1:n/2]`` contains the
    positive-frequency terms, and ``A[n/2:]`` contains the negative-frequency
    terms, in order of decreasingly negative frequency. So ,for an 8-point
    transform, the frequencies of the result are [0, 1, 2, 3, -4, -3, -2, -1].
    To rearrange the fft output so that the zero-frequency component is
    centered, like [-4, -3, -2, -1,  0,  1,  2,  3], use `fftshift`.

    Both single and double precision routines are implemented. Half precision
    inputs will be converted to single precision. Non-floating-point inputs
    will be converted to double precision. Long-double precision inputs are
    not supported.

    This function is most efficient when `n` is a power of two, and least
    efficient when `n` is prime.

    Note that if ``x`` is real-valued, then ``A[j] == A[n-j].conjugate()``.
    If ``x`` is real-valued and ``n`` is even, then ``A[n/2]`` is real.

    If the data type of `x` is real, a "real FFT" algorithm is automatically
    used, which roughly halves the computation time. To increase efficiency
    a little further, use `rfft`, which does the same calculation, but only
    outputs half of the symmetrical spectrum. If the data is both real and
    symmetrical, the `dct` can again double the efficiency by generating
    half of the spectrum from half of the signal.

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.fftpack import fft, ifft
    >>> x = np.arange(5)
    >>> np.allclose(fft(ifft(x)), x, atol=1e-15)  # within numerical accuracy.
    True

    """
    return _duccfft.fft(x, n, axis, None, overwrite_x)


def fft(
    x: Array,
    /,
    xp: Namespace,
    *,
    n: int | None = None,
    axis: int = -1,
    norm: _Norm = "backward",
) -> Array:
    res = xp.fft.fft(x, n=n, axis=axis, norm=norm)
    if x.dtype in [xp.float32, xp.complex64]:
        return res.astype(xp.complex64)
    return res


def fft(a, n=None, axis=-1, norm=None, out=None):
    """
    Compute the one-dimensional discrete Fourier Transform.

    This function computes the one-dimensional *n*-point discrete Fourier
    Transform (DFT) with the efficient Fast Fourier Transform (FFT)
    algorithm [CT]_.

    Parameters
    ----------
    a : array_like
        Input array, can be complex.
    n : int, optional
        Length of the transformed axis of the output.
        If `n` is smaller than the length of the input, the input is cropped.
        If it is larger, the input is padded with zeros.  If `n` is not given,
        the length of the input along the axis specified by `axis` is used.
    axis : int, optional
        Axis over which to compute the FFT.  If not given, the last axis is
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

    Raises
    ------
    IndexError
        If `axis` is not a valid axis of `a`.

    See Also
    --------
    numpy.fft : for definition of the DFT and conventions used.
    ifft : The inverse of `fft`.
    fft2 : The two-dimensional FFT.
    fftn : The *n*-dimensional FFT.
    rfftn : The *n*-dimensional FFT of real input.
    fftfreq : Frequency bins for given FFT parameters.

    Notes
    -----
    FFT (Fast Fourier Transform) refers to a way the discrete Fourier
    Transform (DFT) can be calculated efficiently, by using symmetries in the
    calculated terms.  The symmetry is highest when `n` is a power of 2, and
    the transform is therefore most efficient for these sizes.

    The DFT is defined, with the conventions used in this implementation, in
    the documentation for the `numpy.fft` module.

    References
    ----------
    .. [CT] Cooley, James W., and John W. Tukey, 1965, "An algorithm for the
            machine calculation of complex Fourier series," *Math. Comput.*
            19: 297-301.

    Examples
    --------
    >>> import numpy as np
    >>> np.fft.fft(np.exp(2j * np.pi * np.arange(8) / 8))
    array([-2.33486982e-16+1.14423775e-17j,  8.00000000e+00-1.25557246e-15j,
            2.33486982e-16+2.33486982e-16j,  0.00000000e+00+1.22464680e-16j,
           -1.14423775e-17+2.33486982e-16j,  0.00000000e+00+5.20784380e-16j,
            1.14423775e-17+1.14423775e-17j,  0.00000000e+00+1.22464680e-16j])

    In this example, real input has an FFT which is Hermitian, i.e., symmetric
    in the real part and anti-symmetric in the imaginary part, as described in
    the `numpy.fft` documentation:

    >>> import matplotlib.pyplot as plt
    >>> t = np.arange(256)
    >>> sp = np.fft.fft(np.sin(t))
    >>> freq = np.fft.fftfreq(t.shape[-1])
    >>> _ = plt.plot(freq, sp.real, freq, sp.imag)
    >>> plt.show()

    """
    a = asarray(a)
    if n is None:
        n = a.shape[axis]
    output = _raw_fft(a, n, axis, False, True, norm, out)
    return output


def fft(operand: _ods_ir.Value[_ods_ir.RankedTensorType], fft_type: _Union[_Any, _ods_ir.Attribute], fft_length: _Union[_Union[_Sequence[int], _Buffer], _ods_ir.DenseIntElementsAttr], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return FftOp(operand=operand, fft_type=fft_type, fft_length=fft_length, results=results, loc=loc, ip=ip).result


def fft(operand: _ods_ir.Value[_ods_ir.RankedTensorType], fft_type: _Union[_Any, _ods_ir.Attribute], fft_length: _Union[_Sequence[int], _ods_ir.DenseI64ArrayAttr], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return FftOp(operand=operand, fft_type=fft_type, fft_length=fft_length, results=results, loc=loc, ip=ip).result


def fft(x, fft_type: FftType | str, fft_lengths: Sequence[int]):
  if isinstance(fft_type, str):
    typ = _str_to_fft_type(fft_type)
  elif isinstance(fft_type, FftType):
    typ = fft_type
  else:
    raise TypeError(f"Unknown FFT type value '{fft_type}'")

  if typ == FftType.RFFT:
    if np.iscomplexobj(x):
      raise ValueError("only real valued inputs supported for rfft")
    x = lax.convert_element_type(x, dtypes.to_inexact_dtype(dtypes.dtype(x)))
  else:
    x = lax.convert_element_type(x, dtypes.to_complex_dtype(dtypes.dtype(x)))
  if len(fft_lengths) == 0:
    # XLA FFT doesn't support 0-rank.
    return x
  fft_lengths = tuple(fft_lengths)
  return fft_p.bind(x, fft_type=typ, fft_lengths=fft_lengths)


def fft(a: ArrayLike, n: int | None = None,
        axis: int = -1, norm: str | None = None) -> Array:
  r"""Compute a one-dimensional discrete Fourier transform along a given axis.

  JAX implementation of :func:`numpy.fft.fft`.

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
    - :func:`jax.numpy.fft.ifft`: Computes a one-dimensional inverse discrete
      Fourier transform.
    - :func:`jax.numpy.fft.fftn`: Computes a multidimensional discrete Fourier
      transform.
    - :func:`jax.numpy.fft.ifftn`: Computes a multidimensional inverse discrete
      Fourier transform.

  Examples:
    ``jnp.fft.fft`` computes the transform along ``axis -1`` by default.

    >>> x = jnp.array([[1, 2, 4, 7],
    ...                [5, 3, 1, 9]])
    >>> jnp.fft.fft(x)
    Array([[14.+0.j, -3.+5.j, -4.+0.j, -3.-5.j],
           [18.+0.j,  4.+6.j, -6.+0.j,  4.-6.j]], dtype=complex64)

    When ``n=3``, dimension of the transform along axis -1 will be ``3`` and
    dimension along other axes will be the same as that of input.

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   print(jnp.fft.fft(x, n=3))
    [[ 7.+0.j   -2.+1.73j -2.-1.73j]
     [ 9.+0.j    3.-1.73j  3.+1.73j]]

    When ``n=3`` and ``axis=0``, dimension of the transform along ``axis 0`` will
    be ``3`` and dimension along other axes will be same as that of input.

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   print(jnp.fft.fft(x, n=3, axis=0))
    [[ 6. +0.j    5. +0.j    5. +0.j   16. +0.j  ]
     [-1.5-4.33j  0.5-2.6j   3.5-0.87j  2.5-7.79j]
     [-1.5+4.33j  0.5+2.6j   3.5+0.87j  2.5+7.79j]]

    ``jnp.fft.ifft`` can be used to reconstruct ``x`` from the result of
    ``jnp.fft.fft``.

    >>> x_fft = jnp.fft.fft(x)
    >>> jnp.allclose(x, jnp.fft.ifft(x_fft))
    Array(True, dtype=bool)
  """
  return _fft_core_1d('fft', lax_fft.FftType.FFT, a, n=n, axis=axis,
                      norm=norm)

