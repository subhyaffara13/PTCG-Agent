
def rfftn(a: ArrayLike, s=None, axes=None, norm=None):
    return torch.fft.rfftn(a, s, dim=axes, norm=norm)


def rfftn(
    input: TensorLikeType,
    s: ShapeType | None = None,
    dim: DimsType | None = None,
    norm: NormType = None,
) -> TensorLikeType:
    torch._check(
        not input.dtype.is_complex,
        lambda: f"rfftn expects a real-valued input tensor, but got {input.dtype}",
    )
    shape, dim = _canonicalize_fft_shape_and_dim_args(input, s, dim)
    input = _maybe_promote_tensor_fft(input, require_complex=False)
    input = _resize_fft_input(input, dim, shape)
    out = prims.fft_r2c(input, dim=dim, onesided=True)
    return _apply_norm(out, norm=norm, signal_numel=_prod(shape), forward=True)


def rfftn(x, s=None, axes=None, norm=None, overwrite_x=False, workers=None, *,
          plan=None):
    """
    Compute the N-D discrete Fourier Transform for real input.

    This function computes the N-D discrete Fourier Transform over
    any number of axes in an M-D real array by means of the Fast
    Fourier Transform (FFT). By default, all axes are transformed, with the
    real transform performed over the last axis, while the remaining
    transforms are complex.

    Parameters
    ----------
    x : array_like
        Input array, taken to be real.
    s : sequence of ints, optional
        Shape (length along each transformed axis) to use from the input.
        (``s[0]`` refers to axis 0, ``s[1]`` to axis 1, etc.).
        The final element of `s` corresponds to `n` for ``rfft(x, n)``, while
        for the remaining axes, it corresponds to `n` for ``fft(x, n)``.
        Along any axis, if the given shape is smaller than that of the input,
        the input is cropped. If it is larger, the input is padded with zeros.
        if `s` is not given, the shape of the input along the axes specified
        by `axes` is used.
    axes : sequence of ints, optional
        Axes over which to compute the FFT. If not given, the last ``len(s)``
        axes are used, or all axes if `s` is also not specified.
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
        indicated by `axes`, or by a combination of `s` and `x`,
        as explained in the parameters section above.
        The length of the last axis transformed will be ``s[-1]//2+1``,
        while the remaining transformed axes will have lengths according to
        `s`, or unchanged from the input.

    Raises
    ------
    ValueError
        If `s` and `axes` have different length.
    IndexError
        If an element of `axes` is larger than the number of axes of `x`.

    See Also
    --------
    irfftn : The inverse of `rfftn`, i.e., the inverse of the N-D FFT
         of real input.
    fft : The 1-D FFT, with definitions and conventions used.
    rfft : The 1-D FFT of real input.
    fftn : The N-D FFT.
    rfft2 : The 2-D FFT of real input.

    Notes
    -----
    The transform for real input is performed over the last transformation
    axis, as by `rfft`, then the transform over the remaining axes is
    performed as by `fftn`. The order of the output is as for `rfft` for the
    final transformation axis, and as for `fftn` for the remaining
    transformation axes.

    See `fft` for details, definitions and conventions used.

    Examples
    --------
    >>> import scipy.fft
    >>> import numpy as np
    >>> x = np.ones((2, 2, 2))
    >>> scipy.fft.rfftn(x)
    array([[[8.+0.j,  0.+0.j], # may vary
            [0.+0.j,  0.+0.j]],
           [[0.+0.j,  0.+0.j],
            [0.+0.j,  0.+0.j]]])

    >>> scipy.fft.rfftn(x, axes=(2, 0))
    array([[[4.+0.j,  0.+0.j], # may vary
            [4.+0.j,  0.+0.j]],
           [[0.+0.j,  0.+0.j],
            [0.+0.j,  0.+0.j]]])

    """
    return (Dispatchable(x, np.ndarray),)


def rfftn(x, s=None, axes=None, norm=None,
          overwrite_x=False, workers=None, *, plan=None):
    return _execute_nD('rfftn', _duccfft.rfftn, x, s=s, axes=axes, norm=norm,
                       overwrite_x=overwrite_x, workers=workers, plan=plan)


def rfftn(
    x: Array,
    /,
    xp: Namespace,
    *,
    s: Sequence[int] | None = None,
    axes: Sequence[int] | None = None,
    norm: _Norm = "backward",
) -> Array:
    res = xp.fft.rfftn(x, s=s, axes=axes, norm=norm)
    if x.dtype == xp.float32:
        return res.astype(xp.complex64)
    return res


def rfftn(
    x: Array,
    /,
    *,
    s: Sequence[int] = None,
    axes: Sequence[int] = None,
    norm: Literal["backward", "ortho", "forward"] = "backward",
    **kwargs: object,
) -> Array:
    return torch.fft.rfftn(x, s=s, dim=axes, norm=norm, **kwargs)


def rfftn(a, s=None, axes=None, norm=None, out=None):
    """
    Compute the N-dimensional discrete Fourier Transform for real input.

    This function computes the N-dimensional discrete Fourier Transform over
    any number of axes in an M-dimensional real array by means of the Fast
    Fourier Transform (FFT).  By default, all axes are transformed, with the
    real transform performed over the last axis, while the remaining
    transforms are complex.

    Parameters
    ----------
    a : array_like
        Input array, taken to be real.
    s : sequence of ints, optional
        Shape (length along each transformed axis) to use from the input.
        (``s[0]`` refers to axis 0, ``s[1]`` to axis 1, etc.).
        The final element of `s` corresponds to `n` for ``rfft(x, n)``, while
        for the remaining axes, it corresponds to `n` for ``fft(x, n)``.
        Along any axis, if the given shape is smaller than that of the input,
        the input is cropped. If it is larger, the input is padded with zeros.

        .. versionchanged:: 2.0

            If it is ``-1``, the whole input is used (no padding/trimming).

        If `s` is not given, the shape of the input along the axes specified
        by `axes` is used.

        .. deprecated:: 2.0

            If `s` is not ``None``, `axes` must not be ``None`` either.

        .. deprecated:: 2.0

            `s` must contain only ``int`` s, not ``None`` values. ``None``
            values currently mean that the default value for ``n`` is used
            in the corresponding 1-D transform, but this behaviour is
            deprecated.

    axes : sequence of ints, optional
        Axes over which to compute the FFT.  If not given, the last ``len(s)``
        axes are used, or all axes if `s` is also not specified.

        .. deprecated:: 2.0

            If `s` is specified, the corresponding `axes` to be transformed
            must be explicitly specified too.

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
        indicated by `axes`, or by a combination of `s` and `a`,
        as explained in the parameters section above.
        The length of the last axis transformed will be ``s[-1]//2+1``,
        while the remaining transformed axes will have lengths according to
        `s`, or unchanged from the input.

    Raises
    ------
    ValueError
        If `s` and `axes` have different length.
    IndexError
        If an element of `axes` is larger than than the number of axes of `a`.

    See Also
    --------
    irfftn : The inverse of `rfftn`, i.e. the inverse of the n-dimensional FFT
         of real input.
    fft : The one-dimensional FFT, with definitions and conventions used.
    rfft : The one-dimensional FFT of real input.
    fftn : The n-dimensional FFT.
    rfft2 : The two-dimensional FFT of real input.

    Notes
    -----
    The transform for real input is performed over the last transformation
    axis, as by `rfft`, then the transform over the remaining axes is
    performed as by `fftn`.  The order of the output is as for `rfft` for the
    final transformation axis, and as for `fftn` for the remaining
    transformation axes.

    See `fft` for details, definitions and conventions used.

    Examples
    --------
    >>> import numpy as np
    >>> a = np.ones((2, 2, 2))
    >>> np.fft.rfftn(a)
    array([[[8.+0.j,  0.+0.j], # may vary
            [0.+0.j,  0.+0.j]],
           [[0.+0.j,  0.+0.j],
            [0.+0.j,  0.+0.j]]])

    >>> np.fft.rfftn(a, axes=(2, 0))
    array([[[4.+0.j,  0.+0.j], # may vary
            [4.+0.j,  0.+0.j]],
           [[0.+0.j,  0.+0.j],
            [0.+0.j,  0.+0.j]]])

    """
    a = asarray(a)
    s, axes = _cook_nd_args(a, s, axes)
    a = rfft(a, s[-1], axes[-1], norm, out=out)
    for ii in range(len(axes) - 2, -1, -1):
        a = fft(a, s[ii], axes[ii], norm, out=out)
    return a


def rfftn(a: ArrayLike, s: Shape | None = None,
          axes: Sequence[int] | None = None,
          norm: str | None = None) -> Array:
  """Compute a multidimensional discrete Fourier transform of a real-valued array.

  JAX implementation of :func:`numpy.fft.rfftn`.

  Args:
    a: real-valued input array.
    s: optional sequence of integers. Controls the effective size of the input
      along each specified axis. If not specified, it will default to the
      dimension of input along ``axes``.
    axes: optional sequence of integers, default=None. Specifies the axes along
      which the transform is computed. If not specified, the transform is computed
      along the last ``len(s)`` axes. If neither ``axes`` nor ``s`` is specified,
      the transform is computed along all the axes.
    norm: string, default="backward". The normalization mode. "backward", "ortho"
      and "forward" are supported.

  Returns:
    An array containing the multidimensional discrete Fourier transform of ``a``
    having size specified in ``s`` along the axes ``axes`` except along the axis
    ``axes[-1]``. The size of the output along the axis ``axes[-1]`` is
    ``s[-1]//2+1``.

  See also:
    - :func:`jax.numpy.fft.rfft`: Computes a one-dimensional discrete Fourier
      transform of real-valued array.
    - :func:`jax.numpy.fft.rfft2`: Computes a two-dimensional discrete Fourier
      transform of real-valued array.
    - :func:`jax.numpy.fft.irfftn`: Computes a real-valued multidimensional inverse
      discrete Fourier transform.

  Examples:
    >>> x = jnp.array([[[1, 3, 5],
    ...                 [2, 4, 6]],
    ...                [[7, 9, 11],
    ...                 [8, 10, 12]]])
    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   jnp.fft.rfftn(x)
    Array([[[ 78.+0.j  , -12.+6.93j],
            [ -6.+0.j  ,   0.+0.j  ]],
    <BLANKLINE>
           [[-36.+0.j  ,   0.+0.j  ],
            [  0.+0.j  ,   0.+0.j  ]]], dtype=complex64)

    When ``s=[3, 3, 4]``,  size of the transform along ``axes (-3, -2)`` will
    be (3, 3), and along ``axis -1`` will be ``4//2+1 = 3`` and size along
    other axes will be the same as that of input.

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   jnp.fft.rfftn(x, s=[3, 3, 4])
    Array([[[ 78.   +0.j  , -16.  -26.j  ,  26.   +0.j  ],
            [ 15.  -36.37j, -16.12 +1.93j,   5.  -12.12j],
            [ 15.  +36.37j,   8.12-11.93j,   5.  +12.12j]],
    <BLANKLINE>
           [[ -7.5 -49.36j, -20.45 +9.43j,  -2.5 -16.45j],
            [-25.5  -7.79j,  -0.6 +11.96j,  -8.5  -2.6j ],
            [ 19.5 -12.99j,  -8.33 -6.5j ,   6.5  -4.33j]],
    <BLANKLINE>
           [[ -7.5 +49.36j,  12.45 -4.43j,  -2.5 +16.45j],
            [ 19.5 +12.99j,   0.33 -6.5j ,   6.5  +4.33j],
            [-25.5  +7.79j,   4.6  +5.04j,  -8.5  +2.6j ]]], dtype=complex64)

    When ``s=[3, 5]`` and ``axes=(0, 1)``, size of the transform along ``axis 0``
    will be ``3``, along ``axis 1`` will be ``5//2+1 = 3`` and dimension along
    other axes will be same as that of input.

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   jnp.fft.rfftn(x, s=[3, 5], axes=[0, 1])
    Array([[[ 18.   +0.j  ,  26.   +0.j  ,  34.   +0.j  ],
            [ 11.09 -9.51j,  16.33-13.31j,  21.56-17.12j],
            [ -0.09 -5.88j,   0.67 -8.23j,   1.44-10.58j]],
    <BLANKLINE>
           [[ -4.5 -12.99j,  -2.5 -16.45j,  -0.5 -19.92j],
            [ -9.71 -6.3j , -10.05 -9.52j, -10.38-12.74j],
            [ -4.95 +0.72j,  -5.78 -0.2j ,  -6.61 -1.12j]],
    <BLANKLINE>
           [[ -4.5 +12.99j,  -2.5 +16.45j,  -0.5 +19.92j],
            [  3.47+10.11j,   6.43+11.42j,   9.38+12.74j],
            [  3.19 +1.63j,   4.4  +1.38j,   5.61 +1.12j]]], dtype=complex64)

    For 1-D input:

    >>> x1 = jnp.array([1, 2, 3, 4])
    >>> jnp.fft.rfftn(x1)
    Array([10.+0.j, -2.+2.j, -2.+0.j], dtype=complex64)
  """
  return _fft_core('rfftn', lax_fft.FftType.RFFT, a, s, axes, norm)

