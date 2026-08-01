
def fftn(x):
    """
    Applies n-dimensional Fast Fourier Transform (FFT) to input array.

    Args:
        x: Input n-dimensional array.

    Returns:
        n-dimensional Fourier transform of input n-dimensional array.
    """
    out = x
    for axis in reversed(range(x.ndim)[1:]):  # We don't need to apply FFT to last axis
        out = torch.fft.fft(out, axis=axis)
    return out


def fftn(a: ArrayLike, s=None, axes=None, norm=None):
    return torch.fft.fftn(a, s, dim=axes, norm=norm)


def fftn(
    input: TensorLikeType,
    s: ShapeType | None = None,
    dim: DimsType | None = None,
    norm: NormType = None,
) -> TensorLikeType:
    (shape, dim) = _canonicalize_fft_shape_and_dim_args(input, s, dim)
    x = _maybe_promote_tensor_fft(input, require_complex=True)
    return _fftn_c2c("fftn", x, shape, dim, norm, forward=True)


def fftn(x, s=None, axes=None, norm=None, overwrite_x=False, workers=None, *,
         plan=None):
    """
    Compute the N-D discrete Fourier Transform.

    This function computes the N-D discrete Fourier Transform over
    any number of axes in an M-D array by means of the Fast Fourier
    Transform (FFT).

    Parameters
    ----------
    x : array_like
        Input array, can be complex.
    s : sequence of ints, optional
        Shape (length of each transformed axis) of the output
        (``s[0]`` refers to axis 0, ``s[1]`` to axis 1, etc.).
        This corresponds to ``n`` for ``fft(x, n)``.
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

    Raises
    ------
    ValueError
        If `s` and `axes` have different length.
    IndexError
        If an element of `axes` is larger than the number of axes of `x`.

    See Also
    --------
    ifftn : The inverse of `fftn`, the inverse N-D FFT.
    fft : The 1-D FFT, with definitions and conventions used.
    rfftn : The N-D FFT of real input.
    fft2 : The 2-D FFT.
    fftshift : Shifts zero-frequency terms to centre of array.

    Notes
    -----
    The output, analogously to `fft`, contains the term for zero frequency in
    the low-order corner of all axes, the positive frequency terms in the
    first half of all axes, the term for the Nyquist frequency in the middle
    of all axes and the negative frequency terms in the second half of all
    axes, in order of decreasingly negative frequency.

    Examples
    --------
    >>> import scipy.fft
    >>> import numpy as np
    >>> x = np.mgrid[:3, :3, :3][0]
    >>> scipy.fft.fftn(x, axes=(1, 2))
    array([[[ 0.+0.j,   0.+0.j,   0.+0.j], # may vary
            [ 0.+0.j,   0.+0.j,   0.+0.j],
            [ 0.+0.j,   0.+0.j,   0.+0.j]],
           [[ 9.+0.j,   0.+0.j,   0.+0.j],
            [ 0.+0.j,   0.+0.j,   0.+0.j],
            [ 0.+0.j,   0.+0.j,   0.+0.j]],
           [[18.+0.j,   0.+0.j,   0.+0.j],
            [ 0.+0.j,   0.+0.j,   0.+0.j],
            [ 0.+0.j,   0.+0.j,   0.+0.j]]])
    >>> scipy.fft.fftn(x, (2, 2), axes=(0, 1))
    array([[[ 2.+0.j,  2.+0.j,  2.+0.j], # may vary
            [ 0.+0.j,  0.+0.j,  0.+0.j]],
           [[-2.+0.j, -2.+0.j, -2.+0.j],
            [ 0.+0.j,  0.+0.j,  0.+0.j]]])

    >>> import matplotlib.pyplot as plt
    >>> rng = np.random.default_rng()
    >>> [X, Y] = np.meshgrid(2 * np.pi * np.arange(200) / 12,
    ...                      2 * np.pi * np.arange(200) / 34)
    >>> S = np.sin(X) + np.cos(Y) + rng.uniform(0, 1, X.shape)
    >>> FS = scipy.fft.fftn(S)
    >>> plt.imshow(np.log(np.abs(scipy.fft.fftshift(FS))**2))
    <matplotlib.image.AxesImage object at 0x...>
    >>> plt.show()

    """
    return (Dispatchable(x, np.ndarray),)


def fftn(x, s=None, axes=None, norm=None,
         overwrite_x=False, workers=None, *, plan=None):
    return _execute_nD('fftn', _duccfft.fftn, x, s=s, axes=axes, norm=norm,
                       overwrite_x=overwrite_x, workers=workers, plan=plan)


def fftn(x, shape=None, axes=None, overwrite_x=False):
    """
    Return multidimensional discrete Fourier transform.

    The returned array contains::

      y[j_1,..,j_d] = sum[k_1=0..n_1-1, ..., k_d=0..n_d-1]
         x[k_1,..,k_d] * prod[i=1..d] exp(-sqrt(-1)*2*pi/n_i * j_i * k_i)

    where d = len(x.shape) and n = x.shape.

    Parameters
    ----------
    x : array_like
        The (N-D) array to transform.
    shape : int or array_like of ints or None, optional
        The shape of the result. If both `shape` and `axes` (see below) are
        None, `shape` is ``x.shape``; if `shape` is None but `axes` is
        not None, then `shape` is ``numpy.take(x.shape, axes, axis=0)``.
        If ``shape[i] > x.shape[i]``, the ith dimension is padded with zeros.
        If ``shape[i] < x.shape[i]``, the ith dimension is truncated to
        length ``shape[i]``.
        If any element of `shape` is -1, the size of the corresponding
        dimension of `x` is used.
    axes : int or array_like of ints or None, optional
        The axes of `x` (`y` if `shape` is not None) along which the
        transform is applied.
        The default is over all axes.
    overwrite_x : bool, optional
        If True, the contents of `x` can be destroyed. Default is False.

    Returns
    -------
    y : complex-valued N-D NumPy array
        The (N-D) DFT of the input array.

    See Also
    --------
    ifftn

    Notes
    -----
    If ``x`` is real-valued, then
    ``y[..., j_i, ...] == y[..., n_i-j_i, ...].conjugate()``.

    Both single and double precision routines are implemented. Half precision
    inputs will be converted to single precision. Non-floating-point inputs
    will be converted to double precision. Long-double precision inputs are
    not supported.

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.fftpack import fftn, ifftn
    >>> y = (-np.arange(16), 8 - np.arange(16), np.arange(16))
    >>> np.allclose(y, fftn(ifftn(y)))
    True

    """
    shape = _good_shape(x, shape, axes)
    return _duccfft.fftn(x, shape, axes, None, overwrite_x)


def fftn(
    x: Array,
    /,
    xp: Namespace,
    *,
    s: Sequence[int] | None = None,
    axes: Sequence[int] | None = None,
    norm: _Norm = "backward",
) -> Array:
    res = xp.fft.fftn(x, s=s, axes=axes, norm=norm)
    if x.dtype in [xp.float32, xp.complex64]:
        return res.astype(xp.complex64)
    return res


def fftn(
    x: Array,
    /,
    *,
    s: Sequence[int] = None,
    axes: Sequence[int] = None,
    norm: Literal["backward", "ortho", "forward"] = "backward",
    **kwargs: object,
) -> Array:
    return torch.fft.fftn(x, s=s, dim=axes, norm=norm, **kwargs)


def fftn(a, s=None, axes=None, norm=None, out=None):
    """
    Compute the N-dimensional discrete Fourier Transform.

    This function computes the *N*-dimensional discrete Fourier Transform over
    any number of axes in an *M*-dimensional array by means of the Fast Fourier
    Transform (FFT).

    Parameters
    ----------
    a : array_like
        Input array, can be complex.
    s : sequence of ints, optional
        Shape (length of each transformed axis) of the output
        (``s[0]`` refers to axis 0, ``s[1]`` to axis 1, etc.).
        This corresponds to ``n`` for ``fft(x, n)``.
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
        Repeated indices in `axes` means that the transform over that axis is
        performed multiple times.

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

    Raises
    ------
    ValueError
        If `s` and `axes` have different length.
    IndexError
        If an element of `axes` is larger than than the number of axes of `a`.

    See Also
    --------
    numpy.fft : Overall view of discrete Fourier transforms, with definitions
        and conventions used.
    ifftn : The inverse of `fftn`, the inverse *n*-dimensional FFT.
    fft : The one-dimensional FFT, with definitions and conventions used.
    rfftn : The *n*-dimensional FFT of real input.
    fft2 : The two-dimensional FFT.
    fftshift : Shifts zero-frequency terms to centre of array

    Notes
    -----
    The output, analogously to `fft`, contains the term for zero frequency in
    the low-order corner of all axes, the positive frequency terms in the
    first half of all axes, the term for the Nyquist frequency in the middle
    of all axes and the negative frequency terms in the second half of all
    axes, in order of decreasingly negative frequency.

    See `numpy.fft` for details, definitions and conventions used.

    Examples
    --------
    >>> import numpy as np
    >>> a = np.mgrid[:3, :3, :3][0]
    >>> np.fft.fftn(a, axes=(1, 2))
    array([[[ 0.+0.j,   0.+0.j,   0.+0.j], # may vary
            [ 0.+0.j,   0.+0.j,   0.+0.j],
            [ 0.+0.j,   0.+0.j,   0.+0.j]],
           [[ 9.+0.j,   0.+0.j,   0.+0.j],
            [ 0.+0.j,   0.+0.j,   0.+0.j],
            [ 0.+0.j,   0.+0.j,   0.+0.j]],
           [[18.+0.j,   0.+0.j,   0.+0.j],
            [ 0.+0.j,   0.+0.j,   0.+0.j],
            [ 0.+0.j,   0.+0.j,   0.+0.j]]])
    >>> np.fft.fftn(a, (2, 2), axes=(0, 1))
    array([[[ 2.+0.j,  2.+0.j,  2.+0.j], # may vary
            [ 0.+0.j,  0.+0.j,  0.+0.j]],
           [[-2.+0.j, -2.+0.j, -2.+0.j],
            [ 0.+0.j,  0.+0.j,  0.+0.j]]])

    >>> import matplotlib.pyplot as plt
    >>> [X, Y] = np.meshgrid(2 * np.pi * np.arange(200) / 12,
    ...                      2 * np.pi * np.arange(200) / 34)
    >>> S = np.sin(X) + np.cos(Y) + np.random.uniform(0, 1, X.shape)
    >>> FS = np.fft.fftn(S)
    >>> plt.imshow(np.log(np.abs(np.fft.fftshift(FS))**2))
    <matplotlib.image.AxesImage object at 0x...>
    >>> plt.show()

    """
    return _raw_fftnd(a, s, axes, fft, norm, out=out)


def fftn(a: ArrayLike, s: Shape | None = None,
         axes: Sequence[int] | None = None,
         norm: str | None = None) -> Array:
  r"""Compute a multidimensional discrete Fourier transform along given axes.

  JAX implementation of :func:`numpy.fft.fftn`.

  Args:
    a: input array
    s: sequence of integers. Specifies the shape of the result. If not specified,
      it will default to the shape of ``a`` along the specified ``axes``.
    axes: sequence of integers, default=None. Specifies the axes along which the
      transform is computed.
    norm: string. The normalization mode. "backward", "ortho" and "forward" are
      supported.

  Returns:
    An array containing the multidimensional discrete Fourier transform of ``a``.

  See also:
    - :func:`jax.numpy.fft.fft`: Computes a one-dimensional discrete Fourier
      transform.
    - :func:`jax.numpy.fft.ifft`: Computes a one-dimensional inverse discrete
      Fourier transform.
    - :func:`jax.numpy.fft.ifftn`: Computes a multidimensional inverse discrete
      Fourier transform.

  Examples:
    ``jnp.fft.fftn`` computes the transform along all the axes by default when
    ``axes`` argument is ``None``.

    >>> x = jnp.array([[1, 2, 5, 6],
    ...                [4, 1, 3, 7],
    ...                [5, 9, 2, 1]])
    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   jnp.fft.fftn(x)
    Array([[ 46.  +0.j  ,   0.  +2.j  ,  -6.  +0.j  ,   0.  -2.j  ],
           [ -2.  +1.73j,   6.12+6.73j,   0.  -1.73j, -18.12-3.27j],
           [ -2.  -1.73j, -18.12+3.27j,   0.  +1.73j,   6.12-6.73j]],      dtype=complex64)

    When ``s=[2]``, dimension of the transform along ``axis -1`` will be ``2``
    and dimension along other axes will be the same as that of input.

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   print(jax.numpy.fft.fftn(x, s=[2]))
    [[ 3.+0.j -1.+0.j]
     [ 5.+0.j  3.+0.j]
     [14.+0.j -4.+0.j]]

    When ``s=[2]`` and ``axes=[0]``, dimension of the transform along ``axis 0``
    will be ``2`` and dimension along other axes will be same as that of input.

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   print(jax.numpy.fft.fftn(x, s=[2], axes=[0]))
    [[ 5.+0.j  3.+0.j  8.+0.j 13.+0.j]
     [-3.+0.j  1.+0.j  2.+0.j -1.+0.j]]

    When ``s=[2, 3]``, shape of the transform will be ``(2, 3)``.

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   print(jax.numpy.fft.fftn(x, s=[2, 3]))
    [[16. +0.j   -0.5+4.33j -0.5-4.33j]
     [ 0. +0.j   -4.5+0.87j -4.5-0.87j]]

    ``jnp.fft.ifftn`` can be used to reconstruct ``x`` from the result of
    ``jnp.fft.fftn``.

    >>> x_fftn = jnp.fft.fftn(x)
    >>> jnp.allclose(x, jnp.fft.ifftn(x_fftn))
    Array(True, dtype=bool)
  """
  return _fft_core('fftn', lax_fft.FftType.FFT, a, s, axes, norm)

