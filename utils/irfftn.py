
def irfftn(a: ArrayLike, s=None, axes=None, norm=None):
    return torch.fft.irfftn(a, s, dim=axes, norm=norm)


def irfftn(
    input: TensorLikeType,
    s: ShapeType | None = None,
    dim: DimsType | None = None,
    norm: NormType = None,
) -> TensorLikeType:
    shape, dim, last_dim_size = _canonicalize_fft_c2r_shape_and_dim_args(
        "irfftn", input, s, dim
    )
    input = _maybe_promote_tensor_fft(input, require_complex=True)
    input = _resize_fft_input(input, dim, shape)
    out = prims.fft_c2r(input, dim=dim, last_dim_size=last_dim_size)
    return _apply_norm(out, norm, _prod(out.shape[d] for d in dim), forward=False)


def irfftn(x, s=None, axes=None, norm=None, overwrite_x=False, workers=None, *,
           plan=None):
    """
    Computes the inverse of `rfftn`.

    This function computes the inverse of the N-D discrete
    Fourier Transform for real input over any number of axes in an
    M-D array by means of the Fast Fourier Transform (FFT). In
    other words, ``irfftn(rfftn(x), x.shape) == x`` to within numerical
    accuracy. (The ``a.shape`` is necessary like ``len(a)`` is for `irfft`,
    and for the same reason.)

    The input should be ordered in the same way as is returned by `rfftn`,
    i.e., as for `irfft` for the final transformation axis, and as for `ifftn`
    along all the other axes.

    Parameters
    ----------
    x : array_like
        Input array.
    s : sequence of ints, optional
        Shape (length of each transformed axis) of the output
        (``s[0]`` refers to axis 0, ``s[1]`` to axis 1, etc.). `s` is also the
        number of input points used along this axis, except for the last axis,
        where ``s[-1]//2+1`` points of the input are used.
        Along any axis, if the shape indicated by `s` is smaller than that of
        the input, the input is cropped. If it is larger, the input is padded
        with zeros. If `s` is not given, the shape of the input along the axes
        specified by axes is used. Except for the last axis which is taken to be
        ``2*(m-1)``, where ``m`` is the length of the input along that axis.
    axes : sequence of ints, optional
        Axes over which to compute the inverse FFT. If not given, the last
        `len(s)` axes are used, or all axes if `s` is also not specified.
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
        The truncated or zero-padded input, transformed along the axes
        indicated by `axes`, or by a combination of `s` or `x`,
        as explained in the parameters section above.
        The length of each transformed axis is as given by the corresponding
        element of `s`, or the length of the input in every axis except for the
        last one if `s` is not given. In the final transformed axis the length
        of the output when `s` is not given is ``2*(m-1)``, where ``m`` is the
        length of the final transformed axis of the input. To get an odd
        number of output points in the final axis, `s` must be specified.

    Raises
    ------
    ValueError
        If `s` and `axes` have different length.
    IndexError
        If an element of `axes` is larger than the number of axes of `x`.

    See Also
    --------
    rfftn : The forward N-D FFT of real input,
            of which `ifftn` is the inverse.
    fft : The 1-D FFT, with definitions and conventions used.
    irfft : The inverse of the 1-D FFT of real input.
    irfft2 : The inverse of the 2-D FFT of real input.

    Notes
    -----
    See `fft` for definitions and conventions used.

    See `rfft` for definitions and conventions used for real input.

    The default value of `s` assumes an even output length in the final
    transformation axis. When performing the final complex to real
    transformation, the Hermitian symmetry requires that the last imaginary
    component along that axis must be 0 and so it is ignored. To avoid losing
    information, the correct length of the real input *must* be given.

    Examples
    --------
    >>> import scipy.fft
    >>> import numpy as np
    >>> x = np.zeros((3, 2, 2))
    >>> x[0, 0, 0] = 3 * 2 * 2
    >>> scipy.fft.irfftn(x)
    array([[[1.,  1.],
            [1.,  1.]],
           [[1.,  1.],
            [1.,  1.]],
           [[1.,  1.],
            [1.,  1.]]])

    """
    return (Dispatchable(x, np.ndarray),)


def irfftn(x, s=None, axes=None, norm=None,
           overwrite_x=False, workers=None, *, plan=None):
    return _execute_nD('irfftn', _duccfft.irfftn, x, s=s, axes=axes, norm=norm,
                       overwrite_x=overwrite_x, workers=workers, plan=plan)


def irfftn(
    x: Array,
    /,
    xp: Namespace,
    *,
    s: Sequence[int] | None = None,
    axes: Sequence[int] | None = None,
    norm: _Norm = "backward",
) -> Array:
    res = xp.fft.irfftn(x, s=s, axes=axes, norm=norm)
    if x.dtype == xp.complex64:
        return res.astype(xp.float32)
    return res


def irfftn(
    x: Array,
    /,
    *,
    s: Sequence[int] = None,
    axes: Sequence[int] = None,
    norm: Literal["backward", "ortho", "forward"] = "backward",
    **kwargs: object,
) -> Array:
    return torch.fft.irfftn(x, s=s, dim=axes, norm=norm, **kwargs)


def irfftn(a, s=None, axes=None, norm=None, out=None):
    """
    Computes the inverse of `rfftn`.

    This function computes the inverse of the N-dimensional discrete
    Fourier Transform for real input over any number of axes in an
    M-dimensional array by means of the Fast Fourier Transform (FFT).  In
    other words, ``irfftn(rfftn(a), a.shape) == a`` to within numerical
    accuracy. (The ``a.shape`` is necessary like ``len(a)`` is for `irfft`,
    and for the same reason.)

    The input should be ordered in the same way as is returned by `rfftn`,
    i.e. as for `irfft` for the final transformation axis, and as for `ifftn`
    along all the other axes.

    Parameters
    ----------
    a : array_like
        Input array.
    s : sequence of ints, optional
        Shape (length of each transformed axis) of the output
        (``s[0]`` refers to axis 0, ``s[1]`` to axis 1, etc.). `s` is also the
        number of input points used along this axis, except for the last axis,
        where ``s[-1]//2+1`` points of the input are used.
        Along any axis, if the shape indicated by `s` is smaller than that of
        the input, the input is cropped.  If it is larger, the input is padded
        with zeros.

        .. versionchanged:: 2.0

            If it is ``-1``, the whole input is used (no padding/trimming).

        If `s` is not given, the shape of the input along the axes
        specified by axes is used. Except for the last axis which is taken to
        be ``2*(m-1)`` where ``m`` is the length of the input along that axis.

        .. deprecated:: 2.0

            If `s` is not ``None``, `axes` must not be ``None`` either.

        .. deprecated:: 2.0

            `s` must contain only ``int`` s, not ``None`` values. ``None``
            values currently mean that the default value for ``n`` is used
            in the corresponding 1-D transform, but this behaviour is
            deprecated.

    axes : sequence of ints, optional
        Axes over which to compute the inverse FFT. If not given, the last
        `len(s)` axes are used, or all axes if `s` is also not specified.
        Repeated indices in `axes` means that the inverse transform over that
        axis is performed multiple times.

        .. deprecated:: 2.0

            If `s` is specified, the corresponding `axes` to be transformed
            must be explicitly specified too.

    norm : {"backward", "ortho", "forward"}, optional
        Normalization mode (see `numpy.fft`). Default is "backward".
        Indicates which direction of the forward/backward pair of transforms
        is scaled and with what normalization factor.

        .. versionadded:: 1.20.0

            The "backward", "forward" values were added.

    out : ndarray, optional
        If provided, the result will be placed in this array. It should be
        of the appropriate shape and dtype for the last transformation.

        .. versionadded:: 2.0.0

    Returns
    -------
    out : ndarray
        The truncated or zero-padded input, transformed along the axes
        indicated by `axes`, or by a combination of `s` or `a`,
        as explained in the parameters section above.
        The length of each transformed axis is as given by the corresponding
        element of `s`, or the length of the input in every axis except for the
        last one if `s` is not given.  In the final transformed axis the length
        of the output when `s` is not given is ``2*(m-1)`` where ``m`` is the
        length of the final transformed axis of the input.  To get an odd
        number of output points in the final axis, `s` must be specified.

    Raises
    ------
    ValueError
        If `s` and `axes` have different length.
    IndexError
        If an element of `axes` is larger than than the number of axes of `a`.

    See Also
    --------
    rfftn : The forward n-dimensional FFT of real input,
            of which `ifftn` is the inverse.
    fft : The one-dimensional FFT, with definitions and conventions used.
    irfft : The inverse of the one-dimensional FFT of real input.
    irfft2 : The inverse of the two-dimensional FFT of real input.

    Notes
    -----
    See `fft` for definitions and conventions used.

    See `rfft` for definitions and conventions used for real input.

    The correct interpretation of the hermitian input depends on the shape of
    the original data, as given by `s`. This is because each input shape could
    correspond to either an odd or even length signal. By default, `irfftn`
    assumes an even output length which puts the last entry at the Nyquist
    frequency; aliasing with its symmetric counterpart. When performing the
    final complex to real transform, the last value is thus treated as purely
    real. To avoid losing information, the correct shape of the real input
    **must** be given.

    Examples
    --------
    >>> import numpy as np
    >>> a = np.zeros((3, 2, 2))
    >>> a[0, 0, 0] = 3 * 2 * 2
    >>> np.fft.irfftn(a)
    array([[[1.,  1.],
            [1.,  1.]],
           [[1.,  1.],
            [1.,  1.]],
           [[1.,  1.],
            [1.,  1.]]])

    """
    a = asarray(a)
    s, axes = _cook_nd_args(a, s, axes, invreal=1)
    for ii in range(len(axes) - 1):
        a = ifft(a, s[ii], axes[ii], norm)
    a = irfft(a, s[-1], axes[-1], norm, out=out)
    return a


def irfftn(a: ArrayLike, s: Shape | None = None,
           axes: Sequence[int] | None = None,
           norm: str | None = None) -> Array:
  """Compute a real-valued multidimensional inverse discrete Fourier transform.

  JAX implementation of :func:`numpy.fft.irfftn`.

  Args:
    a: input array.
    s: optional sequence of integers. Specifies the size of the output in each
      specified axis. If not specified, the dimension of output along axis
      ``axes[-1]`` is ``2*(m-1)``, ``m`` is the size of input along axis ``axes[-1]``
      and the dimension along other axes will be the same as that of input.
    axes: optional sequence of integers, default=None. Specifies the axes along
      which the transform is computed. If not specified, the transform is computed
      along the last ``len(s)`` axes. If neither ``axes`` nor ``s`` is specified,
      the transform is computed along all the axes.
    norm: string, default="backward". The normalization mode. "backward", "ortho"
      and "forward" are supported.

  Returns:
    A real-valued array containing the multidimensional inverse discrete Fourier
    transform of ``a`` with size ``s`` along specified ``axes``, and the same as
    the input along other axes.

  See also:
    - :func:`jax.numpy.fft.rfftn`: Computes a multidimensional discrete Fourier
      transform of a real-valued array.
    - :func:`jax.numpy.fft.irfft`: Computes a real-valued one-dimensional inverse
      discrete Fourier transform.
    - :func:`jax.numpy.fft.irfft2`: Computes a real-valued two-dimensional inverse
      discrete Fourier transform.

  Examples:
    ``jnp.fft.irfftn`` computes the transform along all the axes by default.

    >>> x = jnp.array([[[1, 3, 5],
    ...                 [2, 4, 6]],
    ...                [[7, 9, 11],
    ...                 [8, 10, 12]]])
    >>> jnp.fft.irfftn(x)
    Array([[[ 6.5, -1. ,  0. , -1. ],
            [-0.5,  0. ,  0. ,  0. ]],
    <BLANKLINE>
           [[-3. ,  0. ,  0. ,  0. ],
            [ 0. ,  0. ,  0. ,  0. ]]], dtype=float32)

    When ``s=[3, 4]``, size of the transform along ``axes (-2, -1)`` will be
    ``(3, 4)`` and size along other axes will be the same as that of input.

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   jnp.fft.irfftn(x, s=[3, 4])
    Array([[[ 2.33, -0.67,  0.  , -0.67],
            [ 0.33, -0.74,  0.  ,  0.41],
            [ 0.33,  0.41,  0.  , -0.74]],
    <BLANKLINE>
           [[ 6.33, -0.67,  0.  , -0.67],
            [ 1.33, -1.61,  0.  ,  1.28],
            [ 1.33,  1.28,  0.  , -1.61]]], dtype=float32)

    When ``s=[3]`` and ``axes=[0]``, size of the transform along ``axes 0`` will
    be ``3`` and dimension along other axes will be same as that of input.

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   jnp.fft.irfftn(x, s=[3], axes=[0])
    Array([[[ 5.,  7.,  9.],
            [ 6.,  8., 10.]],
    <BLANKLINE>
           [[-2., -2., -2.],
            [-2., -2., -2.]],
    <BLANKLINE>
           [[-2., -2., -2.],
            [-2., -2., -2.]]], dtype=float32)
  """
  return _fft_core('irfftn', lax_fft.FftType.IRFFT, a, s, axes, norm)

