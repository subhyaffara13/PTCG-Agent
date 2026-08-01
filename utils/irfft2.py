
def irfft2(a: ArrayLike, s=None, axes=(-2, -1), norm=None):
    return torch.fft.irfft2(a, s, dim=axes, norm=norm)


def irfft2(
    input: TensorLikeType,
    s: ShapeType | None = None,
    dim: DimsType | None = (-2, -1),
    norm: NormType = None,
) -> TensorLikeType:
    return torch.fft.irfftn(input, s=s, dim=dim, norm=norm)


def irfft2(x, s=None, axes=(-2, -1), norm=None, overwrite_x=False, workers=None, *,
           plan=None):
    """
    Computes the inverse of `rfft2`.

    Parameters
    ----------
    x : array_like
        The input array
    s : sequence of ints, optional
        Shape of the real output to the inverse FFT.
    axes : sequence of ints, optional
        The axes over which to compute the inverse fft.
        Default is the last two axes.
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
        The result of the inverse real 2-D FFT.

    See Also
    --------
    rfft2 : The 2-D FFT of real input.
    irfft : The inverse of the 1-D FFT of real input.
    irfftn : The inverse of the N-D FFT of real input.

    Notes
    -----
    This is really `irfftn` with different defaults.
    For more details see `irfftn`.

    """
    return (Dispatchable(x, np.ndarray),)


def irfft2(x, s=None, axes=(-2, -1), norm=None,
           overwrite_x=False, workers=None, *, plan=None):
    return irfftn(x, s, axes, norm, overwrite_x, workers, plan=plan)


def irfft2(a, s=None, axes=(-2, -1), norm=None, out=None):
    """
    Computes the inverse of `rfft2`.

    Parameters
    ----------
    a : array_like
        The input array
    s : sequence of ints, optional
        Shape of the real output to the inverse FFT.

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
        The axes over which to compute the inverse fft.
        Default: ``(-2, -1)``, the last two axes.

        .. deprecated:: 2.0

            If `s` is specified, the corresponding `axes` to be transformed
            must not be ``None``.

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
        The result of the inverse real 2-D FFT.

    See Also
    --------
    rfft2 : The forward two-dimensional FFT of real input,
            of which `irfft2` is the inverse.
    rfft : The one-dimensional FFT for real input.
    irfft : The inverse of the one-dimensional FFT of real input.
    irfftn : Compute the inverse of the N-dimensional FFT of real input.

    Notes
    -----
    This is really `irfftn` with different defaults.
    For more details see `irfftn`.

    Examples
    --------
    >>> import numpy as np
    >>> a = np.mgrid[:5, :5][0]
    >>> A = np.fft.rfft2(a)
    >>> np.fft.irfft2(A, s=a.shape)
    array([[0., 0., 0., 0., 0.],
           [1., 1., 1., 1., 1.],
           [2., 2., 2., 2., 2.],
           [3., 3., 3., 3., 3.],
           [4., 4., 4., 4., 4.]])
    """
    return irfftn(a, s, axes, norm, out=out)


def irfft2(a: ArrayLike, s: Shape | None = None, axes: Sequence[int] = (-2,-1),
           norm: str | None = None) -> Array:
  """Compute a real-valued two-dimensional inverse discrete Fourier transform.

  JAX implementation of :func:`numpy.fft.irfft2`.

  Args:
    a: input array. Must have ``a.ndim >= 2``.
    s: optional length-2 sequence of integers. Specifies the size of the output
      in each specified axis. If not specified, the dimension of output along
      axis ``axes[1]`` is ``2*(m-1)``, ``m`` is the size of input along axis
      ``axes[1]`` and the dimension along other axes will be the same as that of
      input.
    axes: optional length-2 sequence of integers, default=(-2,-1). Specifies the
      axes along which the transform is computed.
    norm: string, default="backward". The normalization mode. "backward", "ortho"
      and "forward" are supported.

  Returns:
    A real-valued array containing the two-dimensional inverse discrete Fourier
    transform of ``a``.

  See also:
    - :func:`jax.numpy.fft.rfft2`: Computes a two-dimensional discrete Fourier
      transform of a real-valued array.
    - :func:`jax.numpy.fft.irfft`: Computes a real-valued one-dimensional inverse
      discrete Fourier transform.
    - :func:`jax.numpy.fft.irfftn`: Computes a real-valued multidimensional inverse
      discrete Fourier transform.

  Examples:
    ``jnp.fft.irfft2`` computes the transform along the last two axes by default.

    >>> x = jnp.array([[[1, 3, 5],
    ...                 [2, 4, 6]],
    ...                [[7, 9, 11],
    ...                 [8, 10, 12]]])
    >>> jnp.fft.irfft2(x)
    Array([[[ 3.5, -1. ,  0. , -1. ],
            [-0.5,  0. ,  0. ,  0. ]],
    <BLANKLINE>
           [[ 9.5, -1. ,  0. , -1. ],
            [-0.5,  0. ,  0. ,  0. ]]], dtype=float32)

    When ``s=[3, 3]``, dimension of the transform along ``axes (-2, -1)`` will be
    ``(3, 3)`` and dimension along other axes will be the same as that of input.

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   jnp.fft.irfft2(x, s=[3, 3])
    Array([[[ 1.89, -0.44, -0.44],
            [ 0.22, -0.78,  0.56],
            [ 0.22,  0.56, -0.78]],
    <BLANKLINE>
           [[ 5.89, -0.44, -0.44],
            [ 1.22, -1.78,  1.56],
            [ 1.22,  1.56, -1.78]]], dtype=float32)

    When ``s=[2, 3]`` and ``axes=(0, 1)``, shape of the transform along
    ``axes (0, 1)`` will be ``(2, 3)`` and dimension along other axes will be
    same as that of input.

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   jnp.fft.irfft2(x, s=[2, 3], axes=(0, 1))
    Array([[[ 4.67,  6.67,  8.67],
            [-0.33, -0.33, -0.33],
            [-0.33, -0.33, -0.33]],
    <BLANKLINE>
           [[-3.  , -3.  , -3.  ],
            [ 0.  ,  0.  ,  0.  ],
            [ 0.  ,  0.  ,  0.  ]]], dtype=float32)
  """
  return _fft_core_2d('irfft2', lax_fft.FftType.IRFFT, a, s=s, axes=axes,
                      norm=norm)

