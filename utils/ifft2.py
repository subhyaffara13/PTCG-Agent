
def ifft2(a: ArrayLike, s=None, axes=(-2, -1), norm=None):
    return torch.fft.ifft2(a, s, dim=axes, norm=norm)


def ifft2(
    input: TensorLikeType,
    s: ShapeType | None = None,
    dim: DimsType | None = (-2, -1),
    norm: NormType = None,
) -> TensorLikeType:
    return torch.fft.ifftn(input, s=s, dim=dim, norm=norm)


def ifft2(x, s=None, axes=(-2, -1), norm=None, overwrite_x=False, workers=None, *,
          plan=None):
    """
    Compute the 2-D inverse discrete Fourier Transform.

    This function computes the inverse of the 2-D discrete Fourier
    Transform over any number of axes in an M-D array by means of
    the Fast Fourier Transform (FFT). In other words, ``ifft2(fft2(x)) == x``
    to within numerical accuracy. By default, the inverse transform is
    computed over the last two axes of the input array.

    The input, analogously to `ifft`, should be ordered in the same way as is
    returned by `fft2`, i.e., it should have the term for zero frequency
    in the low-order corner of the two axes, the positive frequency terms in
    the first half of these axes, the term for the Nyquist frequency in the
    middle of the axes and the negative frequency terms in the second half of
    both axes, in order of decreasingly negative frequency.

    Parameters
    ----------
    x : array_like
        Input array, can be complex.
    s : sequence of ints, optional
        Shape (length of each axis) of the output (``s[0]`` refers to axis 0,
        ``s[1]`` to axis 1, etc.). This corresponds to `n` for ``ifft(x, n)``.
        Along each axis, if the given shape is smaller than that of the input,
        the input is cropped. If it is larger, the input is padded with zeros.
        if `s` is not given, the shape of the input along the axes specified
        by `axes` is used.  See notes for issue on `ifft` zero padding.
    axes : sequence of ints, optional
        Axes over which to compute the FFT. If not given, the last two
        axes are used.
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
        The truncated or zero-padded input, transformed along the axes
        indicated by `axes`, or the last two axes if `axes` is not given.

    Raises
    ------
    ValueError
        If `s` and `axes` have different length, or `axes` not given and
        ``len(s) != 2``.
    IndexError
        If an element of `axes` is larger than the number of axes of `x`.

    See Also
    --------
    fft2 : The forward 2-D FFT, of which `ifft2` is the inverse.
    ifftn : The inverse of the N-D FFT.
    fft : The 1-D FFT.
    ifft : The 1-D inverse FFT.

    Notes
    -----
    `ifft2` is just `ifftn` with a different default for `axes`.

    See `ifftn` for details and a plotting example, and `fft` for
    definition and conventions used.

    Zero-padding, analogously with `ifft`, is performed by appending zeros to
    the input along the specified dimension. Although this is the common
    approach, it might lead to surprising results. If another form of zero
    padding is desired, it must be performed before `ifft2` is called.

    Examples
    --------
    >>> import scipy.fft
    >>> import numpy as np
    >>> x = 4 * np.eye(4)
    >>> scipy.fft.ifft2(x)
    array([[1.+0.j,  0.+0.j,  0.+0.j,  0.+0.j], # may vary
           [0.+0.j,  0.+0.j,  0.+0.j,  1.+0.j],
           [0.+0.j,  0.+0.j,  1.+0.j,  0.+0.j],
           [0.+0.j,  1.+0.j,  0.+0.j,  0.+0.j]])

    """
    return (Dispatchable(x, np.ndarray),)


def ifft2(x, s=None, axes=(-2, -1), norm=None,
          overwrite_x=False, workers=None, *, plan=None):
    return ifftn(x, s, axes, norm, overwrite_x, workers, plan=plan)


def ifft2(x, shape=None, axes=(-2,-1), overwrite_x=False):
    """
    2-D discrete inverse Fourier transform of real or complex sequence.

    Return inverse 2-D discrete Fourier transform of
    arbitrary type sequence x.

    See `ifft` for more information.

    See Also
    --------
    fft2, ifft

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.fftpack import fft2, ifft2
    >>> y = np.mgrid[:5, :5][0]
    >>> y
    array([[0, 0, 0, 0, 0],
           [1, 1, 1, 1, 1],
           [2, 2, 2, 2, 2],
           [3, 3, 3, 3, 3],
           [4, 4, 4, 4, 4]])
    >>> np.allclose(y, fft2(ifft2(y)))
    True

    """  # numpydoc ignore=RT01
    return ifftn(x,shape,axes,overwrite_x)


def ifft2(a, s=None, axes=(-2, -1), norm=None, out=None):
    """
    Compute the 2-dimensional inverse discrete Fourier Transform.

    This function computes the inverse of the 2-dimensional discrete Fourier
    Transform over any number of axes in an M-dimensional array by means of
    the Fast Fourier Transform (FFT).  In other words, ``ifft2(fft2(a)) == a``
    to within numerical accuracy.  By default, the inverse transform is
    computed over the last two axes of the input array.

    The input, analogously to `ifft`, should be ordered in the same way as is
    returned by `fft2`, i.e. it should have the term for zero frequency
    in the low-order corner of the two axes, the positive frequency terms in
    the first half of these axes, the term for the Nyquist frequency in the
    middle of the axes and the negative frequency terms in the second half of
    both axes, in order of decreasingly negative frequency.

    Parameters
    ----------
    a : array_like
        Input array, can be complex.
    s : sequence of ints, optional
        Shape (length of each axis) of the output (``s[0]`` refers to axis 0,
        ``s[1]`` to axis 1, etc.).  This corresponds to `n` for ``ifft(x, n)``.
        Along each axis, if the given shape is smaller than that of the input,
        the input is cropped. If it is larger, the input is padded with zeros.

        .. versionchanged:: 2.0

            If it is ``-1``, the whole input is used (no padding/trimming).

        If `s` is not given, the shape of the input along the axes specified
        by `axes` is used.  See notes for issue on `ifft` zero padding.

        .. deprecated:: 2.0

            If `s` is not ``None``, `axes` must not be ``None`` either.

        .. deprecated:: 2.0

            `s` must contain only ``int`` s, not ``None`` values. ``None``
            values currently mean that the default value for ``n`` is used
            in the corresponding 1-D transform, but this behaviour is
            deprecated.

    axes : sequence of ints, optional
        Axes over which to compute the FFT.  If not given, the last two
        axes are used.  A repeated index in `axes` means the transform over
        that axis is performed multiple times.  A one-element sequence means
        that a one-dimensional FFT is performed. Default: ``(-2, -1)``.

        .. deprecated:: 2.0

            If `s` is specified, the corresponding `axes` to be transformed
            must not be ``None``.

    norm : {"backward", "ortho", "forward"}, optional
        Normalization mode (see `numpy.fft`). Default is "backward".
        Indicates which direction of the forward/backward pair of transforms
        is scaled and with what normalization factor.

        .. versionadded:: 1.20.0

            The "backward", "forward" values were added.

    out : complex ndarray, optional
        If provided, the result will be placed in this array. It should be
        of the appropriate shape and dtype for all axes (and hence is
        incompatible with passing in all but the trivial ``s``).

        .. versionadded:: 2.0.0

    Returns
    -------
    out : complex ndarray
        The truncated or zero-padded input, transformed along the axes
        indicated by `axes`, or the last two axes if `axes` is not given.

    Raises
    ------
    ValueError
        If `s` and `axes` have different length, or `axes` not given and
        ``len(s) != 2``.
    IndexError
        If an element of `axes` is larger than than the number of axes of `a`.

    See Also
    --------
    numpy.fft : Overall view of discrete Fourier transforms, with definitions
         and conventions used.
    fft2 : The forward 2-dimensional FFT, of which `ifft2` is the inverse.
    ifftn : The inverse of the *n*-dimensional FFT.
    fft : The one-dimensional FFT.
    ifft : The one-dimensional inverse FFT.

    Notes
    -----
    `ifft2` is just `ifftn` with a different default for `axes`.

    See `ifftn` for details and a plotting example, and `numpy.fft` for
    definition and conventions used.

    Zero-padding, analogously with `ifft`, is performed by appending zeros to
    the input along the specified dimension.  Although this is the common
    approach, it might lead to surprising results.  If another form of zero
    padding is desired, it must be performed before `ifft2` is called.

    Examples
    --------
    >>> import numpy as np
    >>> a = 4 * np.eye(4)
    >>> np.fft.ifft2(a)
    array([[1.+0.j,  0.+0.j,  0.+0.j,  0.+0.j], # may vary
           [0.+0.j,  0.+0.j,  0.+0.j,  1.+0.j],
           [0.+0.j,  0.+0.j,  1.+0.j,  0.+0.j],
           [0.+0.j,  1.+0.j,  0.+0.j,  0.+0.j]])

    """
    return _raw_fftnd(a, s, axes, ifft, norm, out=out)


def ifft2(a: ArrayLike, s: Shape | None = None, axes: Sequence[int] = (-2,-1),
          norm: str | None = None) -> Array:
  """Compute a two-dimensional inverse discrete Fourier transform.

  JAX implementation of :func:`numpy.fft.ifft2`.

  Args:
    a: input array. Must have ``a.ndim >= 2``.
    s: optional length-2 sequence of integers. Specifies the size of the output
      in each specified axis. If not specified, it will default to the size of
      ``a`` along the specified ``axes``.
    axes: optional length-2 sequence of integers, default=(-2,-1). Specifies the
      axes along which the transform is computed.
    norm: string, default="backward". The normalization mode. "backward", "ortho"
      and "forward" are supported.

  Returns:
    An array containing the two-dimensional inverse discrete Fourier transform
    of ``a`` along given ``axes``.

  See also:
    - :func:`jax.numpy.fft.ifft`: Computes a one-dimensional inverse discrete
      Fourier transform.
    - :func:`jax.numpy.fft.ifftn`: Computes a multidimensional inverse discrete
      Fourier transform.
    - :func:`jax.numpy.fft.fft2`: Computes a two-dimensional discrete Fourier
      transform.

  Examples:
    ``jnp.fft.ifft2`` computes the transform along the last two axes by default.

    >>> x = jnp.array([[[1, 3],
    ...                 [2, 4]],
    ...                [[5, 7],
    ...                 [6, 8]]])
    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   jnp.fft.ifft2(x)
    Array([[[ 2.5+0.j, -1. +0.j],
            [-0.5+0.j,  0. +0.j]],
    <BLANKLINE>
           [[ 6.5+0.j, -1. +0.j],
            [-0.5+0.j,  0. +0.j]]], dtype=complex64)

    When ``s=[2, 3]``, dimension of the transform along ``axes (-2, -1)`` will be
    ``(2, 3)`` and dimension along other axes will be the same as that of input.

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   jnp.fft.ifft2(x, s=[2, 3])
    Array([[[ 1.67+0.j  , -0.08+1.01j, -0.08-1.01j],
            [-0.33+0.j  , -0.08-0.14j, -0.08+0.14j]],
    <BLANKLINE>
           [[ 4.33+0.j  ,  0.58+2.17j,  0.58-2.17j],
            [-0.33+0.j  , -0.08-0.14j, -0.08+0.14j]]], dtype=complex64)

    When ``s=[2, 3]`` and ``axes=(0, 1)``, shape of the transform along
    ``axes (0, 1)`` will be ``(2, 3)`` and dimension along other axes will be
    same as that of input.

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   jnp.fft.ifft2(x, s=[2, 3], axes=(0, 1))
    Array([[[ 2.33+0.j  ,  3.67+0.j  ],
            [ 0.33+1.15j,  0.67+1.73j],
            [ 0.33-1.15j,  0.67-1.73j]],
    <BLANKLINE>
           [[-1.33+0.j  , -1.33+0.j  ],
            [-0.33-0.58j, -0.33-0.58j],
            [-0.33+0.58j, -0.33+0.58j]]], dtype=complex64)
  """
  return _fft_core_2d('ifft2', lax_fft.FftType.IFFT, a, s=s, axes=axes,
                      norm=norm)

