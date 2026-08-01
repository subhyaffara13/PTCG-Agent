
def rfft2(a: ArrayLike, s=None, axes=(-2, -1), norm=None):
    return torch.fft.rfft2(a, s, dim=axes, norm=norm)


def rfft2(
    input: TensorLikeType,
    s: ShapeType | None = None,
    dim: DimsType | None = (-2, -1),
    norm: NormType = None,
) -> TensorLikeType:
    return torch.fft.rfftn(input, s=s, dim=dim, norm=norm)


def rfft2(x, s=None, axes=(-2, -1), norm=None, overwrite_x=False, workers=None, *,
          plan=None):
    """
    Compute the 2-D FFT of a real array.

    Parameters
    ----------
    x : array
        Input array, taken to be real.
    s : sequence of ints, optional
        Shape of the FFT.
    axes : sequence of ints, optional
        Axes over which to compute the FFT.
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
        The result of the real 2-D FFT.

    See Also
    --------
    irfft2 : The inverse of the 2-D FFT of real input.
    rfft : The 1-D FFT of real input.
    rfftn : Compute the N-D discrete Fourier Transform for real
            input.

    Notes
    -----
    This is really just `rfftn` with different default behavior.
    For more details see `rfftn`.

    Examples
    --------
    >>> import scipy.fft
    >>> import numpy as np
    >>> x = np.broadcast_to([1, 0, -1, 0], (4, 4))
    >>> scipy.fft.rfft2(x)
    array([[0.+0.j, 8.+0.j, 0.+0.j],
           [0.+0.j, 0.+0.j, 0.+0.j],
           [0.+0.j, 0.+0.j, 0.+0.j],
           [0.+0.j, 0.+0.j, 0.+0.j]])

    """
    return (Dispatchable(x, np.ndarray),)


def rfft2(x, s=None, axes=(-2, -1), norm=None,
         overwrite_x=False, workers=None, *, plan=None):
    return rfftn(x, s, axes, norm, overwrite_x, workers, plan=plan)


def rfft2(a, s=None, axes=(-2, -1), norm=None, out=None):
    """
    Compute the 2-dimensional FFT of a real array.

    Parameters
    ----------
    a : array
        Input array, taken to be real.
    s : sequence of ints, optional
        Shape of the FFT.

        .. versionchanged:: 2.0

            If it is ``-1``, the whole input is used (no padding/trimming).

        .. deprecated:: 2.0

            If `s` is not ``None``, `axes` must not be ``None`` either.

        .. deprecated:: 2.0

            `s` must contain only ``int`` s, not ``None`` values. ``None``
            values currently mean that the default value for ``n`` is used
            in the corresponding 1-D transform, but this behaviour is
            deprecated.

    axes : sequence of ints, optional
        Axes over which to compute the FFT. Default: ``(-2, -1)``.

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
        of the appropriate shape and dtype for the last inverse transform.
        incompatible with passing in all but the trivial ``s``).

        .. versionadded:: 2.0.0

    Returns
    -------
    out : ndarray
        The result of the real 2-D FFT.

    See Also
    --------
    rfftn : Compute the N-dimensional discrete Fourier Transform for real
            input.

    Notes
    -----
    This is really just `rfftn` with different default behavior.
    For more details see `rfftn`.

    Examples
    --------
    >>> import numpy as np
    >>> a = np.mgrid[:5, :5][0]
    >>> np.fft.rfft2(a)
    array([[ 50.  +0.j        ,   0.  +0.j        ,   0.  +0.j        ],
           [-12.5+17.20477401j,   0.  +0.j        ,   0.  +0.j        ],
           [-12.5 +4.0614962j ,   0.  +0.j        ,   0.  +0.j        ],
           [-12.5 -4.0614962j ,   0.  +0.j        ,   0.  +0.j        ],
           [-12.5-17.20477401j,   0.  +0.j        ,   0.  +0.j        ]])
    """
    return rfftn(a, s, axes, norm, out=out)


def rfft2(a: ArrayLike, s: Shape | None = None, axes: Sequence[int] = (-2,-1),
          norm: str | None = None) -> Array:
  """Compute a two-dimensional discrete Fourier transform of a real-valued array.

  JAX implementation of :func:`numpy.fft.rfft2`.

  Args:
    a: real-valued input array. Must have ``a.ndim >= 2``.
    s: optional length-2 sequence of integers. Specifies the effective size of the
      output along each specified axis. If not specified, it will default to the
      dimension of input along ``axes``.
    axes: optional length-2 sequence of integers, default=(-2,-1). Specifies the
      axes along which the transform is computed.
    norm: string, default="backward". The normalization mode. "backward", "ortho"
      and "forward" are supported.

  Returns:
    An array containing the two-dimensional discrete Fourier transform of ``a``.
    The size of the output along the axis ``axes[1]`` is ``(s[1]/2)+1``, if ``s[1]``
    is even and ``(s[1]+1)/2``, if ``s[1]`` is odd. The size of the output along
    the axis ``axes[0]`` is ``s[0]``.

  See also:
    - :func:`jax.numpy.fft.rfft`: Computes a one-dimensional discrete Fourier
      transform of real-valued array.
    - :func:`jax.numpy.fft.rfftn`: Computes a multidimensional discrete Fourier
      transform of real-valued array.
    - :func:`jax.numpy.fft.irfft2`: Computes a real-valued two-dimensional inverse
      discrete Fourier transform.

  Examples:
    ``jnp.fft.rfft2`` computes the transform along the last two axes by default.

    >>> x = jnp.array([[[1, 3, 5],
    ...                 [2, 4, 6]],
    ...                [[7, 9, 11],
    ...                 [8, 10, 12]]])
    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   jnp.fft.rfft2(x)
    Array([[[21.+0.j  , -6.+3.46j],
            [-3.+0.j  ,  0.+0.j  ]],
    <BLANKLINE>
           [[57.+0.j  , -6.+3.46j],
            [-3.+0.j  ,  0.+0.j  ]]], dtype=complex64)

    When ``s=[2, 4]``, dimension of the transform along ``axis -2`` will be
    ``2``, along ``axis -1`` will be ``(4/2)+1) = 3`` and dimension along other
    axes will be the same as that of input.

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   jnp.fft.rfft2(x, s=[2, 4])
    Array([[[21. +0.j, -8. -7.j,  7. +0.j],
            [-3. +0.j,  0. +1.j, -1. +0.j]],
    <BLANKLINE>
           [[57. +0.j, -8.-19.j, 19. +0.j],
            [-3. +0.j,  0. +1.j, -1. +0.j]]], dtype=complex64)

    When ``s=[3, 5]`` and ``axes=(0, 1)``, shape of the transform along ``axis 0``
    will be ``3``, along ``axis 1`` will be ``(5+1)/2 = 3`` and dimension along
    other axes will be same as that of input.

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   jnp.fft.rfft2(x, s=[3, 5], axes=(0, 1))
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
  """
  return _fft_core_2d('rfft2', lax_fft.FftType.RFFT, a, s=s, axes=axes,
                      norm=norm)

