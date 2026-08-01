
def fft2(a: ArrayLike, s=None, axes=(-2, -1), norm=None):
    return torch.fft.fft2(a, s, dim=axes, norm=norm)


def fft2(
    input: TensorLikeType,
    s: ShapeType | None = None,
    dim: DimsType | None = (-2, -1),
    norm: NormType = None,
) -> TensorLikeType:
    return torch.fft.fftn(input, s=s, dim=dim, norm=norm)


def fft2(x, s=None, axes=(-2, -1), norm=None, overwrite_x=False, workers=None, *,
         plan=None):
    """
    Compute the 2-D discrete Fourier Transform.

    This function computes the N-D discrete Fourier Transform
    over any axes in an M-D array by means of the
    Fast Fourier Transform (FFT). By default, the transform is computed over
    the last two axes of the input array, i.e., a 2-dimensional FFT.

    Parameters
    ----------
    x : array_like
        Input array, can be complex
    s : sequence of ints, optional
        Shape (length of each transformed axis) of the output
        (``s[0]`` refers to axis 0, ``s[1]`` to axis 1, etc.).
        This corresponds to ``n`` for ``fft(x, n)``.
        Along each axis, if the given shape is smaller than that of the input,
        the input is cropped. If it is larger, the input is padded with zeros.
        if `s` is not given, the shape of the input along the axes specified
        by `axes` is used.
    axes : sequence of ints, optional
        Axes over which to compute the FFT. If not given, the last two axes are
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
    ifft2 : The inverse 2-D FFT.
    fft : The 1-D FFT.
    fftn : The N-D FFT.
    fftshift : Shifts zero-frequency terms to the center of the array.
        For 2-D input, swaps first and third quadrants, and second
        and fourth quadrants.

    Notes
    -----
    `fft2` is just `fftn` with a different default for `axes`.

    The output, analogously to `fft`, contains the term for zero frequency in
    the low-order corner of the transformed axes, the positive frequency terms
    in the first half of these axes, the term for the Nyquist frequency in the
    middle of the axes and the negative frequency terms in the second half of
    the axes, in order of decreasingly negative frequency.

    See `fftn` for details and a plotting example, and `fft` for
    definitions and conventions used.


    Examples
    --------
    >>> import scipy.fft
    >>> import numpy as np
    >>> x = np.mgrid[:5, :5][0]
    >>> scipy.fft.fft2(x)
    array([[ 50.  +0.j        ,   0.  +0.j        ,   0.  +0.j        , # may vary
              0.  +0.j        ,   0.  +0.j        ],
           [-12.5+17.20477401j,   0.  +0.j        ,   0.  +0.j        ,
              0.  +0.j        ,   0.  +0.j        ],
           [-12.5 +4.0614962j ,   0.  +0.j        ,   0.  +0.j        ,
              0.  +0.j        ,   0.  +0.j        ],
           [-12.5 -4.0614962j ,   0.  +0.j        ,   0.  +0.j        ,
              0.  +0.j        ,   0.  +0.j        ],
           [-12.5-17.20477401j,   0.  +0.j        ,   0.  +0.j        ,
              0.  +0.j        ,   0.  +0.j        ]])

    """
    return (Dispatchable(x, np.ndarray),)


def fft2(x, s=None, axes=(-2, -1), norm=None,
         overwrite_x=False, workers=None, *, plan=None):
    return fftn(x, s, axes, norm, overwrite_x, workers, plan=plan)


def fft2(x, shape=None, axes=(-2,-1), overwrite_x=False):
    """
    2-D discrete Fourier transform.

    Return the 2-D discrete Fourier transform of the 2-D argument
    `x`.

    See Also
    --------
    fftn : for detailed information.

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
    >>> np.allclose(y, ifft2(fft2(y)))
    True
    """  # numpydoc ignore=RT01
    return fftn(x,shape,axes,overwrite_x)


def fft2(a, s=None, axes=(-2, -1), norm=None, out=None):
    """
    Compute the 2-dimensional discrete Fourier Transform.

    This function computes the *n*-dimensional discrete Fourier Transform
    over any axes in an *M*-dimensional array by means of the
    Fast Fourier Transform (FFT).  By default, the transform is computed over
    the last two axes of the input array, i.e., a 2-dimensional FFT.

    Parameters
    ----------
    a : array_like
        Input array, can be complex
    s : sequence of ints, optional
        Shape (length of each transformed axis) of the output
        (``s[0]`` refers to axis 0, ``s[1]`` to axis 1, etc.).
        This corresponds to ``n`` for ``fft(x, n)``.
        Along each axis, if the given shape is smaller than that of the input,
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
        of the appropriate shape and dtype for all axes (and hence only the
        last axis can have ``s`` not equal to the shape at that axis).

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
    ifft2 : The inverse two-dimensional FFT.
    fft : The one-dimensional FFT.
    fftn : The *n*-dimensional FFT.
    fftshift : Shifts zero-frequency terms to the center of the array.
        For two-dimensional input, swaps first and third quadrants, and second
        and fourth quadrants.

    Notes
    -----
    `fft2` is just `fftn` with a different default for `axes`.

    The output, analogously to `fft`, contains the term for zero frequency in
    the low-order corner of the transformed axes, the positive frequency terms
    in the first half of these axes, the term for the Nyquist frequency in the
    middle of the axes and the negative frequency terms in the second half of
    the axes, in order of decreasingly negative frequency.

    See `fftn` for details and a plotting example, and `numpy.fft` for
    definitions and conventions used.


    Examples
    --------
    >>> import numpy as np
    >>> a = np.mgrid[:5, :5][0]
    >>> np.fft.fft2(a)
    array([[ 50.  +0.j        ,   0.  +0.j        ,   0.  +0.j        , # may vary
              0.  +0.j        ,   0.  +0.j        ],
           [-12.5+17.20477401j,   0.  +0.j        ,   0.  +0.j        ,
              0.  +0.j        ,   0.  +0.j        ],
           [-12.5 +4.0614962j ,   0.  +0.j        ,   0.  +0.j        ,
              0.  +0.j        ,   0.  +0.j        ],
           [-12.5 -4.0614962j ,   0.  +0.j        ,   0.  +0.j        ,
              0.  +0.j        ,   0.  +0.j        ],
           [-12.5-17.20477401j,   0.  +0.j        ,   0.  +0.j        ,
              0.  +0.j        ,   0.  +0.j        ]])

    """
    return _raw_fftnd(a, s, axes, fft, norm, out=out)


def fft2(a: ArrayLike, s: Shape | None = None, axes: Sequence[int] = (-2,-1),
         norm: str | None = None) -> Array:
  """Compute a two-dimensional discrete Fourier transform along given axes.

  JAX implementation of :func:`numpy.fft.fft2`.

  Args:
    a: input array. Must have ``a.ndim >= 2``.
    s: optional length-2 sequence of integers. Specifies the size of the output
      along each specified axis. If not specified, it will default to the size
      of ``a`` along the specified ``axes``.
    axes: optional length-2 sequence of integers, default=(-2,-1). Specifies the
      axes along which the transform is computed.
    norm: string, default="backward". The normalization mode. "backward", "ortho"
      and "forward" are supported.

  Returns:
    An array containing the two-dimensional discrete Fourier transform of ``a``
    along given ``axes``.

  See also:
    - :func:`jax.numpy.fft.fft`: Computes a one-dimensional discrete Fourier
      transform.
    - :func:`jax.numpy.fft.fftn`: Computes a multidimensional discrete Fourier
      transform.
    - :func:`jax.numpy.fft.ifft2`: Computes a two-dimensional inverse discrete
      Fourier transform.

  Examples:
    ``jnp.fft.fft2`` computes the transform along the last two axes by default.

    >>> x = jnp.array([[[1, 3],
    ...                 [2, 4]],
    ...                [[5, 7],
    ...                 [6, 8]]])
    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   jnp.fft.fft2(x)
    Array([[[10.+0.j, -4.+0.j],
            [-2.+0.j,  0.+0.j]],
    <BLANKLINE>
           [[26.+0.j, -4.+0.j],
            [-2.+0.j,  0.+0.j]]], dtype=complex64)

    When ``s=[2, 3]``, dimension of the transform along ``axes (-2, -1)`` will be
    ``(2, 3)`` and dimension along other axes will be the same as that of input.

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   jnp.fft.fft2(x, s=[2, 3])
    Array([[[10.  +0.j  , -0.5 -6.06j, -0.5 +6.06j],
            [-2.  +0.j  , -0.5 +0.87j, -0.5 -0.87j]],
    <BLANKLINE>
           [[26.  +0.j  ,  3.5-12.99j,  3.5+12.99j],
            [-2.  +0.j  , -0.5 +0.87j, -0.5 -0.87j]]], dtype=complex64)

    When ``s=[2, 3]`` and ``axes=(0, 1)``, shape of the transform along
    ``axes (0, 1)`` will be ``(2, 3)`` and dimension along other axes will be
    same as that of input.

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   jnp.fft.fft2(x, s=[2, 3], axes=(0, 1))
    Array([[[14. +0.j  , 22. +0.j  ],
            [ 2. -6.93j,  4.-10.39j],
            [ 2. +6.93j,  4.+10.39j]],
    <BLANKLINE>
           [[-8. +0.j  , -8. +0.j  ],
            [-2. +3.46j, -2. +3.46j],
            [-2. -3.46j, -2. -3.46j]]], dtype=complex64)

    ``jnp.fft.ifft2`` can be used to reconstruct ``x`` from the result of
    ``jnp.fft.fft2``.

    >>> x_fft2 = jnp.fft.fft2(x)
    >>> jnp.allclose(x, jnp.fft.ifft2(x_fft2))
    Array(True, dtype=bool)
  """
  return _fft_core_2d('fft2', lax_fft.FftType.FFT, a, s=s, axes=axes,
                      norm=norm)

