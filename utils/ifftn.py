
def ifftn(a: ArrayLike, s=None, axes=None, norm=None):
    return torch.fft.ifftn(a, s, dim=axes, norm=norm)


def ifftn(
    input: TensorLikeType,
    s: ShapeType | None = None,
    dim: DimsType | None = None,
    norm: NormType = None,
) -> TensorLikeType:
    (shape, dim) = _canonicalize_fft_shape_and_dim_args(input, s, dim)
    x = _maybe_promote_tensor_fft(input, require_complex=True)
    return _fftn_c2c("ifftn", x, shape, dim, norm, forward=False)


def ifftn(x, s=None, axes=None, norm=None, overwrite_x=False, workers=None, *,
          plan=None):
    """
    Compute the N-D inverse discrete Fourier Transform.

    This function computes the inverse of the N-D discrete
    Fourier Transform over any number of axes in an M-D array by
    means of the Fast Fourier Transform (FFT).  In other words,
    ``ifftn(fftn(x)) == x`` to within numerical accuracy.

    The input, analogously to `ifft`, should be ordered in the same way as is
    returned by `fftn`, i.e., it should have the term for zero frequency
    in all axes in the low-order corner, the positive frequency terms in the
    first half of all axes, the term for the Nyquist frequency in the middle
    of all axes and the negative frequency terms in the second half of all
    axes, in order of decreasingly negative frequency.

    Parameters
    ----------
    x : array_like
        Input array, can be complex.
    s : sequence of ints, optional
        Shape (length of each transformed axis) of the output
        (``s[0]`` refers to axis 0, ``s[1]`` to axis 1, etc.).
        This corresponds to ``n`` for ``ifft(x, n)``.
        Along any axis, if the given shape is smaller than that of the input,
        the input is cropped. If it is larger, the input is padded with zeros.
        if `s` is not given, the shape of the input along the axes specified
        by `axes` is used. See notes for issue on `ifft` zero padding.
    axes : sequence of ints, optional
        Axes over which to compute the IFFT.  If not given, the last ``len(s)``
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
        indicated by `axes`, or by a combination of `s` or `x`,
        as explained in the parameters section above.

    Raises
    ------
    ValueError
        If `s` and `axes` have different length.
    IndexError
        If an element of `axes` is larger than the number of axes of `x`.

    See Also
    --------
    fftn : The forward N-D FFT, of which `ifftn` is the inverse.
    ifft : The 1-D inverse FFT.
    ifft2 : The 2-D inverse FFT.
    ifftshift : Undoes `fftshift`, shifts zero-frequency terms to beginning
        of array.

    Notes
    -----
    Zero-padding, analogously with `ifft`, is performed by appending zeros to
    the input along the specified dimension. Although this is the common
    approach, it might lead to surprising results. If another form of zero
    padding is desired, it must be performed before `ifftn` is called.

    Examples
    --------
    >>> import scipy.fft
    >>> import numpy as np
    >>> x = np.eye(4)
    >>> scipy.fft.ifftn(scipy.fft.fftn(x, axes=(0,)), axes=(1,))
    array([[1.+0.j,  0.+0.j,  0.+0.j,  0.+0.j], # may vary
           [0.+0.j,  1.+0.j,  0.+0.j,  0.+0.j],
           [0.+0.j,  0.+0.j,  1.+0.j,  0.+0.j],
           [0.+0.j,  0.+0.j,  0.+0.j,  1.+0.j]])


    Create and plot an image with band-limited frequency content:

    >>> import matplotlib.pyplot as plt
    >>> rng = np.random.default_rng()
    >>> n = np.zeros((200,200), dtype=complex)
    >>> n[60:80, 20:40] = np.exp(1j*rng.uniform(0, 2*np.pi, (20, 20)))
    >>> im = scipy.fft.ifftn(n).real
    >>> plt.imshow(im)
    <matplotlib.image.AxesImage object at 0x...>
    >>> plt.show()

    """
    return (Dispatchable(x, np.ndarray),)


def ifftn(x, s=None, axes=None, norm=None,
          overwrite_x=False, workers=None, *, plan=None):
    return _execute_nD('ifftn', _duccfft.ifftn, x, s=s, axes=axes, norm=norm,
                       overwrite_x=overwrite_x, workers=workers, plan=plan)


def ifftn(x, shape=None, axes=None, overwrite_x=False):
    """
    Return inverse multidimensional discrete Fourier transform.

    The sequence can be of an arbitrary type.

    The returned array contains::

      y[j_1,..,j_d] = 1/p * sum[k_1=0..n_1-1, ..., k_d=0..n_d-1]
         x[k_1,..,k_d] * prod[i=1..d] exp(sqrt(-1)*2*pi/n_i * j_i * k_i)

    where ``d = len(x.shape)``, ``n = x.shape``, and ``p = prod[i=1..d] n_i``.

    For description of parameters see `fftn`.

    See Also
    --------
    fftn : for detailed information.

    Examples
    --------
    >>> from scipy.fftpack import fftn, ifftn
    >>> import numpy as np
    >>> y = (-np.arange(16), 8 - np.arange(16), np.arange(16))
    >>> np.allclose(y, ifftn(fftn(y)))
    True

    """  # numpydoc ignore=RT01
    shape = _good_shape(x, shape, axes)
    return _duccfft.ifftn(x, shape, axes, None, overwrite_x)


def ifftn(
    x: Array,
    /,
    xp: Namespace,
    *,
    s: Sequence[int] | None = None,
    axes: Sequence[int] | None = None,
    norm: _Norm = "backward",
) -> Array:
    res = xp.fft.ifftn(x, s=s, axes=axes, norm=norm)
    if x.dtype in [xp.float32, xp.complex64]:
        return res.astype(xp.complex64)
    return res


def ifftn(
    x: Array,
    /,
    *,
    s: Sequence[int] = None,
    axes: Sequence[int] = None,
    norm: Literal["backward", "ortho", "forward"] = "backward",
    **kwargs: object,
) -> Array:
    return torch.fft.ifftn(x, s=s, dim=axes, norm=norm, **kwargs)


def ifftn(a, s=None, axes=None, norm=None, out=None):
    """
    Compute the N-dimensional inverse discrete Fourier Transform.

    This function computes the inverse of the N-dimensional discrete
    Fourier Transform over any number of axes in an M-dimensional array by
    means of the Fast Fourier Transform (FFT).  In other words,
    ``ifftn(fftn(a)) == a`` to within numerical accuracy.
    For a description of the definitions and conventions used, see `numpy.fft`.

    The input, analogously to `ifft`, should be ordered in the same way as is
    returned by `fftn`, i.e. it should have the term for zero frequency
    in all axes in the low-order corner, the positive frequency terms in the
    first half of all axes, the term for the Nyquist frequency in the middle
    of all axes and the negative frequency terms in the second half of all
    axes, in order of decreasingly negative frequency.

    Parameters
    ----------
    a : array_like
        Input array, can be complex.
    s : sequence of ints, optional
        Shape (length of each transformed axis) of the output
        (``s[0]`` refers to axis 0, ``s[1]`` to axis 1, etc.).
        This corresponds to ``n`` for ``ifft(x, n)``.
        Along any axis, if the given shape is smaller than that of the input,
        the input is cropped. If it is larger, the input is padded with zeros.

        .. versionchanged:: 2.0

            If it is ``-1``, the whole input is used (no padding/trimming).

        If `s` is not given, the shape of the input along the axes specified
        by `axes` is used. See notes for issue on `ifft` zero padding.

        .. deprecated:: 2.0

            If `s` is not ``None``, `axes` must not be ``None`` either.

        .. deprecated:: 2.0

            `s` must contain only ``int`` s, not ``None`` values. ``None``
            values currently mean that the default value for ``n`` is used
            in the corresponding 1-D transform, but this behaviour is
            deprecated.

    axes : sequence of ints, optional
        Axes over which to compute the IFFT.  If not given, the last ``len(s)``
        axes are used, or all axes if `s` is also not specified.
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

    out : complex ndarray, optional
        If provided, the result will be placed in this array. It should be
        of the appropriate shape and dtype for all axes (and hence is
        incompatible with passing in all but the trivial ``s``).

        .. versionadded:: 2.0.0

    Returns
    -------
    out : complex ndarray
        The truncated or zero-padded input, transformed along the axes
        indicated by `axes`, or by a combination of `s` or `a`,
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
    fftn : The forward *n*-dimensional FFT, of which `ifftn` is the inverse.
    ifft : The one-dimensional inverse FFT.
    ifft2 : The two-dimensional inverse FFT.
    ifftshift : Undoes `fftshift`, shifts zero-frequency terms to beginning
        of array.

    Notes
    -----
    See `numpy.fft` for definitions and conventions used.

    Zero-padding, analogously with `ifft`, is performed by appending zeros to
    the input along the specified dimension.  Although this is the common
    approach, it might lead to surprising results.  If another form of zero
    padding is desired, it must be performed before `ifftn` is called.

    Examples
    --------
    >>> import numpy as np
    >>> a = np.eye(4)
    >>> np.fft.ifftn(np.fft.fftn(a, axes=(0,)), axes=(1,))
    array([[1.+0.j,  0.+0.j,  0.+0.j,  0.+0.j], # may vary
           [0.+0.j,  1.+0.j,  0.+0.j,  0.+0.j],
           [0.+0.j,  0.+0.j,  1.+0.j,  0.+0.j],
           [0.+0.j,  0.+0.j,  0.+0.j,  1.+0.j]])


    Create and plot an image with band-limited frequency content:

    >>> import matplotlib.pyplot as plt
    >>> n = np.zeros((200,200), dtype=np.complex128)
    >>> n[60:80, 20:40] = np.exp(1j*np.random.uniform(0, 2*np.pi, (20, 20)))
    >>> im = np.fft.ifftn(n).real
    >>> plt.imshow(im)
    <matplotlib.image.AxesImage object at 0x...>
    >>> plt.show()

    """
    return _raw_fftnd(a, s, axes, ifft, norm, out=out)


def ifftn(a: ArrayLike, s: Shape | None = None,
          axes: Sequence[int] | None = None,
          norm: str | None = None) -> Array:
  r"""Compute a multidimensional inverse discrete Fourier transform.

  JAX implementation of :func:`numpy.fft.ifftn`.

  Args:
    a: input array
    s: sequence of integers. Specifies the shape of the result. If not specified,
      it will default to the shape of ``a`` along the specified ``axes``.
    axes: sequence of integers, default=None. Specifies the axes along which the
      transform is computed. If None, computes the transform along all the axes.
    norm: string. The normalization mode. "backward", "ortho" and "forward" are
      supported.

  Returns:
    An array containing the multidimensional inverse discrete Fourier transform
    of ``a``.

  See also:
    - :func:`jax.numpy.fft.fftn`: Computes a multidimensional discrete Fourier
      transform.
    - :func:`jax.numpy.fft.fft`: Computes a one-dimensional discrete Fourier
      transform.
    - :func:`jax.numpy.fft.ifft`: Computes a one-dimensional inverse discrete
      Fourier transform.

  Examples:
    ``jnp.fft.ifftn`` computes the transform along all the axes by default when
    ``axes`` argument is ``None``.

    >>> x = jnp.array([[1, 2, 5, 3],
    ...                [4, 1, 2, 6],
    ...                [5, 3, 2, 1]])
    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   print(jnp.fft.ifftn(x))
    [[ 2.92+0.j    0.08-0.33j  0.25+0.j    0.08+0.33j]
     [-0.08+0.14j -0.04-0.03j  0.  -0.29j -1.05-0.11j]
     [-0.08-0.14j -1.05+0.11j  0.  +0.29j -0.04+0.03j]]

    When ``s=[3]``, dimension of the transform along ``axis -1`` will be ``3``
    and dimension along other axes will be the same as that of input.

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   print(jnp.fft.ifftn(x, s=[3]))
    [[ 2.67+0.j   -0.83-0.87j -0.83+0.87j]
     [ 2.33+0.j    0.83-0.29j  0.83+0.29j]
     [ 3.33+0.j    0.83+0.29j  0.83-0.29j]]

    When ``s=[2]`` and ``axes=[0]``, dimension of the transform along ``axis 0``
    will be ``2`` and dimension along other axes will be same as that of input.

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   print(jnp.fft.ifftn(x, s=[2], axes=[0]))
    [[ 2.5+0.j  1.5+0.j  3.5+0.j  4.5+0.j]
     [-1.5+0.j  0.5+0.j  1.5+0.j -1.5+0.j]]

    When ``s=[2, 3]``, shape of the transform will be ``(2, 3)``.

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   print(jnp.fft.ifftn(x, s=[2, 3]))
    [[ 2.5 +0.j    0.  -0.58j  0.  +0.58j]
     [ 0.17+0.j   -0.83-0.29j -0.83+0.29j]]
  """
  return _fft_core('ifftn', lax_fft.FftType.IFFT, a, s, axes, norm)

