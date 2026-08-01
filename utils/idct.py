
def idct(x, type=2, n=None, axis=-1, norm=None, overwrite_x=False,
         workers=None, orthogonalize=None):
    """
    Return the Inverse Discrete Cosine Transform of an arbitrary type sequence.

    Parameters
    ----------
    x : array_like
        The input array.
    type : {1, 2, 3, 4}, optional
        Type of the DCT (see Notes). Default type is 2.
    n : int, optional
        Length of the transform.  If ``n < x.shape[axis]``, `x` is
        truncated.  If ``n > x.shape[axis]``, `x` is zero-padded. The
        default results in ``n = x.shape[axis]``.
    axis : int, optional
        Axis along which the idct is computed; the default is over the
        last axis (i.e., ``axis=-1``).
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
    idct : ndarray of real
        The transformed input array.

    See Also
    --------
    dct : Forward DCT

    Notes
    -----
    For a single dimension array `x`, ``idct(x, norm='ortho')`` is equal to
    MATLAB ``idct(x)``.

    .. warning:: For ``type in {1, 2, 3}``, ``norm="ortho"`` breaks the direct
                 correspondence with the inverse direct Fourier transform. To
                 recover it you must specify ``orthogonalize=False``.

    For ``norm="ortho"`` both the `dct` and `idct` are scaled by the same
    overall factor in both directions. By default, the transform is also
    orthogonalized which for types 1, 2 and 3 means the transform definition is
    modified to give orthogonality of the IDCT matrix (see `dct` for the full
    definitions).

    'The' IDCT is the IDCT-II, which is the same as the normalized DCT-III.

    The IDCT is equivalent to a normal DCT except for the normalization and
    type. DCT type 1 and 4 are their own inverse and DCTs 2 and 3 are each
    other's inverses.

    Examples
    --------
    The Type 1 DCT is equivalent to the DFT for real, even-symmetrical
    inputs. The output is also real and even-symmetrical. Half of the IFFT
    input is used to generate half of the IFFT output:

    >>> from scipy.fft import ifft, idct
    >>> import numpy as np
    >>> ifft(np.array([ 30.,  -8.,   6.,  -2.,   6.,  -8.])).real
    array([  4.,   3.,   5.,  10.,   5.,   3.])
    >>> idct(np.array([ 30.,  -8.,   6.,  -2.]), 1)
    array([  4.,   3.,   5.,  10.])

    """
    return (Dispatchable(x, np.ndarray),)


def idct(x, type=2, n=None, axis=-1, norm=None,
         overwrite_x=False, workers=None, orthogonalize=None):
    return _execute(_duccfft.idct, x, type, n, axis, norm, 
                    overwrite_x, workers, orthogonalize)


def idct(x, type=2, n=None, axis=-1, norm=None, overwrite_x=False):
    """
    Return the Inverse Discrete Cosine Transform of an arbitrary type sequence.

    Parameters
    ----------
    x : array_like
        The input array.
    type : {1, 2, 3, 4}, optional
        Type of the DCT (see Notes). Default type is 2.
    n : int, optional
        Length of the transform.  If ``n < x.shape[axis]``, `x` is
        truncated.  If ``n > x.shape[axis]``, `x` is zero-padded. The
        default results in ``n = x.shape[axis]``.
    axis : int, optional
        Axis along which the idct is computed; the default is over the
        last axis (i.e., ``axis=-1``).
    norm : {None, 'ortho'}, optional
        Normalization mode (see Notes). Default is None.
    overwrite_x : bool, optional
        If True, the contents of `x` can be destroyed; the default is False.

    Returns
    -------
    idct : ndarray of real
        The transformed input array.

    See Also
    --------
    dct : Forward DCT

    Notes
    -----
    For a single dimension array `x`, ``idct(x, norm='ortho')`` is equal to
    MATLAB ``idct(x)``.

    'The' IDCT is the IDCT of type 2, which is the same as DCT of type 3.

    IDCT of type 1 is the DCT of type 1, IDCT of type 2 is the DCT of type
    3, and IDCT of type 3 is the DCT of type 2. IDCT of type 4 is the DCT
    of type 4. For the definition of these types, see `dct`.

    Examples
    --------
    The Type 1 DCT is equivalent to the DFT for real, even-symmetrical
    inputs. The output is also real and even-symmetrical. Half of the IFFT
    input is used to generate half of the IFFT output:

    >>> from scipy.fftpack import ifft, idct
    >>> import numpy as np
    >>> ifft(np.array([ 30.,  -8.,   6.,  -2.,   6.,  -8.])).real
    array([  4.,   3.,   5.,  10.,   5.,   3.])
    >>> idct(np.array([ 30.,  -8.,   6.,  -2.]), 1) / 6
    array([  4.,   3.,   5.,  10.])

    """
    type = _inverse_typemap[type]
    return _duccfft.dct(x, type, n, axis, norm, overwrite_x)


def idct(x: Array, type: int = 2, n: int | None = None,
         axis: int = -1, norm: str | None = None) -> Array:
  """Computes the inverse discrete cosine transform of the input

  JAX implementation of :func:`scipy.fft.idct`.

  Args:
    x: array
    type: integer, default = 2. Currently only type 2 is supported.
    n: integer, default = x.shape[axis]. The length of the transform.
      If larger than ``x.shape[axis]``, the input will be zero-padded, if
      smaller, the input will be truncated.
    axis: integer, default=-1. The axis along which the dct will be performed.
    norm: string. The normalization mode: one of ``[None, "backward", "ortho"]``.
      The default is ``None``, which is equivalent to ``"backward"``.

  Returns:
    array containing the inverse discrete cosine transform of x

  See Also:
    - :func:`jax.scipy.fft.dct`: DCT
    - :func:`jax.scipy.fft.dctn`: multidimensional DCT
    - :func:`jax.scipy.fft.idctn`: multidimensional inverse DCT

  Examples:

    >>> x = jax.random.normal(jax.random.key(0), (3, 3))
    >>> with jnp.printoptions(precision=2, suppress=True):
    ...    print(jax.scipy.fft.idct(x))
    [[ 0.78  0.41 -0.39]
     [-0.12  0.31 -0.23]
     [ 0.17 -0.3  -0.11]]

    When ``n`` smaller than ``x.shape[axis]``

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...    print(jax.scipy.fft.idct(x, n=2))
    [[ 1.12 -0.31]
     [ 0.04 -0.08]
     [ 0.05 -0.3 ]]

    When ``n`` smaller than ``x.shape[axis]`` and ``axis=0``

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...    print(jax.scipy.fft.idct(x, n=2, axis=0))
    [[ 0.38  0.57 -0.45]
     [ 0.43  0.44  0.24]]

    When ``n`` larger than ``x.shape[axis]`` and ``axis=0``

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...    print(jax.scipy.fft.idct(x, n=4, axis=0))
    [[ 0.1   0.38 -0.16]
     [ 0.28  0.18 -0.26]
     [ 0.3   0.15 -0.08]
     [ 0.13  0.3   0.29]]

    ``jax.scipy.fft.idct`` can be used to reconstruct ``x`` from the result
    of ``jax.scipy.fft.dct``

    >>> x_dct = jax.scipy.fft.dct(x)
    >>> jnp.allclose(x, jax.scipy.fft.idct(x_dct))
    Array(True, dtype=bool)
  """
  x = ensure_arraylike("idct", x)

  if type != 2:
    raise NotImplementedError('Only DCT type 2 is implemented.')
  if norm is not None and norm not in ['backward', 'ortho']:
    raise ValueError(f"jax.scipy.fft.idct: {norm=!r} is not implemented")

  if dtypes.issubdtype(x.dtype, np.complexfloating):
    return lax.complex(
      idct(x.real, type=type, n=n, norm=norm, axis=axis),
      idct(x.imag, type=type, n=n, norm=norm, axis=axis)
    )

  axis = canonicalize_axis(axis, x.ndim)
  if n is not None:
    x = lax.pad(x, jnp.array(0, x.dtype),
                [(0, n - x.shape[axis] if a == axis else 0, 0)
                 for a in range(x.ndim)])
  N = x.shape[axis]
  x, = promote_dtypes_inexact(x)
  if norm is None or norm == 'backward':
    x = _dct_ortho_norm(x, axis)
  x = _dct_ortho_norm(x, axis)

  k = lax.expand_dims(jnp.arange(N, dtype=x.dtype), [a for a in range(x.ndim) if a != axis])
  # everything is complex from here...
  w4 = _W4(N,k)
  x = x.astype(w4.dtype)
  x = x / (_W4(N, k))
  x = x * 2 * N

  x = jnp_fft.ifft(x, axis=axis)
  # convert back to reals..
  out = _dct_deinterleave(x.real, axis)
  return out

