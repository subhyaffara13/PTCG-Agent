
def idctn(x, type=2, s=None, axes=None, norm=None, overwrite_x=False,
          workers=None, orthogonalize=None):
    """
    Return multidimensional Inverse Discrete Cosine Transform along the specified axes.

    Parameters
    ----------
    x : array_like
        The input array.
    type : {1, 2, 3, 4}, optional
        Type of the DCT (see Notes). Default type is 2.
    s : int or array_like of ints or None, optional
        The shape of the result.  If both `s` and `axes` (see below) are
        None, `s` is ``x.shape``; if `s` is None but `axes` is
        not None, then `s` is ``numpy.take(x.shape, axes, axis=0)``.
        If ``s[i] > x.shape[i]``, the ith dimension of the input is padded with zeros.
        If ``s[i] < x.shape[i]``, the ith dimension of the input is truncated to length
        ``s[i]``.
        If any element of `s` is -1, the size of the corresponding dimension of
        `x` is used.
    axes : int or array_like of ints or None, optional
        Axes over which the IDCT is computed. If not given, the last ``len(s)``
        axes are used, or all axes if `s` is also not specified.
    norm : {"backward", "ortho", "forward"}, optional
        Normalization mode (see Notes). Default is "backward".
    overwrite_x : bool, optional
        If True, the contents of `x` can be destroyed; the default is False.
    workers : int, optional
        Maximum number of workers to use for parallel computation. If negative,
        the value wraps around from ``os.cpu_count()``.
        See :func:`~scipy.fft.fft` for more details.
    orthogonalize : bool, optional
        Whether to use the orthogonalized IDCT variant (see Notes).
        Defaults to ``True`` when ``norm="ortho"`` and ``False`` otherwise.

        .. versionadded:: 1.8.0

    Returns
    -------
    y : ndarray of real
        The transformed input array.

    See Also
    --------
    dctn : multidimensional DCT

    Notes
    -----
    For full details of the IDCT types and normalization modes, as well as
    references, see `idct`.

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.fft import dctn, idctn
    >>> rng = np.random.default_rng()
    >>> y = rng.standard_normal((16, 16))
    >>> np.allclose(y, idctn(dctn(y)))
    True

    """
    return (Dispatchable(x, np.ndarray),)


def idctn(x, type=2, s=None, axes=None, norm=None,
          overwrite_x=False, workers=None, *, orthogonalize=None):
    return _execute(_duccfft.idctn, x, type, s, axes, norm, 
                    overwrite_x, workers, orthogonalize)


def idctn(x, type=2, shape=None, axes=None, norm=None, overwrite_x=False):
    """
    Return multidimensional Discrete Cosine Transform along the specified axes.

    Parameters
    ----------
    x : array_like
        The input array.
    type : {1, 2, 3, 4}, optional
        Type of the DCT (see Notes). Default type is 2.
    shape : int or array_like of ints or None, optional
        The shape of the result.  If both `shape` and `axes` (see below) are
        None, `shape` is ``x.shape``; if `shape` is None but `axes` is
        not None, then `shape` is ``numpy.take(x.shape, axes, axis=0)``.
        If ``shape[i] > x.shape[i]``, the ith dimension is padded with zeros.
        If ``shape[i] < x.shape[i]``, the ith dimension is truncated to
        length ``shape[i]``.
        If any element of `shape` is -1, the size of the corresponding
        dimension of `x` is used.
    axes : int or array_like of ints or None, optional
        Axes along which the IDCT is computed.
        The default is over all axes.
    norm : {None, 'ortho'}, optional
        Normalization mode (see Notes). Default is None.
    overwrite_x : bool, optional
        If True, the contents of `x` can be destroyed; the default is False.

    Returns
    -------
    y : ndarray of real
        The transformed input array.

    See Also
    --------
    dctn : multidimensional DCT

    Notes
    -----
    For full details of the IDCT types and normalization modes, as well as
    references, see `idct`.

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.fftpack import dctn, idctn
    >>> rng = np.random.default_rng()
    >>> y = rng.standard_normal((16, 16))
    >>> np.allclose(y, idctn(dctn(y, norm='ortho'), norm='ortho'))
    True

    """
    type = _inverse_typemap[type]
    shape = _good_shape(x, shape, axes)
    return _duccfft.dctn(x, type, shape, axes, norm, overwrite_x)


def idctn(x: Array, type: int = 2,
          s: Sequence[int] | None=None,
          axes: Sequence[int] | None = None,
          norm: str | None = None) -> Array:
  """Computes the multidimensional inverse discrete cosine transform of the input

  JAX implementation of :func:`scipy.fft.idctn`.

  Args:
    x: array
    type: integer, default = 2. Currently only type 2 is supported.
    s: integer or sequence of integers. Specifies the shape of the result. If
      not specified, it will default to the shape of ``x`` along the specified
      ``axes``.
    axes: integer or sequence of integers. Specifies the axes along which the
      transform will be computed. If not given, the last ``len(s)`` axes are
      used, or all axes if ``s`` is also not specified.
    norm: string. The normalization mode: one of
      ``[None, "backward", "ortho"]``. The default is ``None``, which is
      equivalent to ``"backward"``.

  Returns:
    array containing the inverse discrete cosine transform of x

  See Also:
    - :func:`jax.scipy.fft.dct`: one-dimensional DCT
    - :func:`jax.scipy.fft.dctn`: multidimensional DCT
    - :func:`jax.scipy.fft.idct`: one-dimensional inverse DCT

  Examples:

    ``jax.scipy.fft.idctn`` computes the transform along both the axes by
    default when ``axes`` argument is ``None`` and ``s`` is also ``None``.

    >>> x = jax.random.normal(jax.random.key(0), (3, 3))
    >>> with jnp.printoptions(precision=2, suppress=True):
    ...    print(jax.scipy.fft.idctn(x))
    [[ 0.12  0.11 -0.15]
     [ 0.07  0.17 -0.03]
     [ 0.19 -0.07 -0.02]]

    When ``s=[2]``, the transform will be computed only along the last axis,
    with its dimension padded or truncated to size ``2``:

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...  print(jax.scipy.fft.idctn(x, s=[2]))
    [[ 1.12 -0.31]
     [ 0.04 -0.08]
     [ 0.05 -0.3 ]]

    When ``s=[2]`` and ``axes=[0]``, the transform will be computed only along
    the specified axis, with its dimension padded or truncated to size ``2``:

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...  print(jax.scipy.fft.idctn(x, s=[2], axes=[0]))
    [[ 0.38  0.57 -0.45]
     [ 0.43  0.44  0.24]]

    When ``s=[2, 4]``, shape of the transform will be ``(2, 4)``

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...  print(jax.scipy.fft.idctn(x, s=[2, 4]))
    [[ 0.1   0.18  0.07 -0.16]
     [ 0.2   0.06 -0.03 -0.01]]

    ``jax.scipy.fft.idctn`` can be used to reconstruct ``x`` from the result
    of ``jax.scipy.fft.dctn``

    >>> x_dctn = jax.scipy.fft.dctn(x)
    >>> jnp.allclose(x, jax.scipy.fft.idctn(x_dctn))
    Array(True, dtype=bool)
  """
  x = ensure_arraylike("idctn", x)

  if type != 2:
    raise NotImplementedError('Only DCT type 2 is implemented.')
  if norm is not None and norm not in ['backward', 'ortho']:
    raise ValueError(f"jax.scipy.fft.idctn: {norm=!r} is not implemented")

  if dtypes.issubdtype(x.dtype, np.complexfloating):
    return lax.complex(
      idctn(x.real, type=type, s=s, norm=norm, axes=axes),
      idctn(x.imag, type=type, s=s, norm=norm, axes=axes)
    )

  if s is not None:
    try:
      s = list(s)
    except TypeError:
      assert not isinstance(s, Sequence)
      s = [operator.index(s)]
    if len(s) > x.ndim:
      raise ValueError(
          f"s must have at most x.ndim ({x.ndim}) elements, got {len(s)}"
      )

  if axes is None:
    if s is not None:
      axes = tuple(range(x.ndim - len(s), x.ndim))
    else:
      axes = tuple(range(x.ndim))
  else:
    axes = canonicalize_axis_tuple(axes, x.ndim)

  if len(axes) == 1:
    return idct(x, n=s[0] if s is not None else None, axis=axes[0], norm=norm)

  if s is not None:
    ns = dict(zip(axes, s))
    pads = [(0, ns[a] - x.shape[a] if a in ns else 0, 0) for a in range(x.ndim)]
    x = lax.pad(x, jnp.array(0, x.dtype), pads)

  # compose high-D DCTs from 1D DCTs:
  for axis in axes:
    x = idct(x, axis=axis, norm=norm)
  return x

