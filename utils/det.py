
def det(a: ArrayLike):
    a = _atleast_float_1(a)
    return torch.linalg.det(a)


def det(matexpr):
    """ Matrix Determinant

    Examples
    ========

    >>> from sympy import MatrixSymbol, det, eye
    >>> A = MatrixSymbol('A', 3, 3)
    >>> det(A)
    Determinant(A)
    >>> det(eye(3))
    1
    """

    return Determinant(matexpr).doit()


def det(a, overwrite_a=False, check_finite=True):
    """
    Compute the determinant of a matrix.

    The determinant is a scalar that is a function of the associated square
    matrix coefficients. The determinant value is zero for singular matrices.

    Array argument(s) of this function may have additional
    "batch" dimensions prepended to the core shape. In this case, the array is treated
    as a batch of lower-dimensional slices; see :ref:`linalg_batch` for details.

    Parameters
    ----------
    a : (..., M, M) array_like
        Input array to compute determinants for.
    overwrite_a : bool, optional
        Allow overwriting data in a (may enhance performance).
        See :ref:`tutorial_linalg_overwrite` for details.
    check_finite : bool, optional
        Whether to check that the input matrix contains only finite numbers.
        Disabling may give a performance gain, but may result in problems
        (crashes, non-termination) if the inputs do contain infinities or NaNs.

    Returns
    -------
    det : (...) float or complex
        Determinant of `a`. For stacked arrays, a scalar is returned for each
        (m, m) slice in the last two dimensions of the input. For example, an
        input of shape (p, q, m, m) will produce a result of shape (p, q). If
        all dimensions are 1 a scalar is returned regardless of ndim.

    Notes
    -----
    The determinant is computed by performing an LU factorization of the
    input with LAPACK routine 'getrf', and then calculating the product of
    diagonal entries of the U factor.

    Even if the input array is single precision (float32 or complex64), the
    result will be returned in double precision (float64 or complex128) to
    prevent overflows.

    Examples
    --------
    >>> import numpy as np
    >>> from scipy import linalg
    >>> a = np.array([[1,2,3], [4,5,6], [7,8,9]])  # A singular matrix
    >>> linalg.det(a)
    0.0
    >>> b = np.array([[0,2,3], [4,5,6], [7,8,9]])
    >>> linalg.det(b)
    3.0
    >>> # An array with the shape (3, 2, 2, 2)
    >>> c = np.array([[[[1., 2.], [3., 4.]],
    ...                [[5., 6.], [7., 8.]]],
    ...               [[[9., 10.], [11., 12.]],
    ...                [[13., 14.], [15., 16.]]],
    ...               [[[17., 18.], [19., 20.]],
    ...                [[21., 22.], [23., 24.]]]])
    >>> linalg.det(c)  # The resulting shape is (3, 2)
    array([[-2., -2.],
           [-2., -2.],
           [-2., -2.]])
    >>> linalg.det(c[0, 0])  # Confirm the (0, 0) slice, [[1, 2], [3, 4]]
    -2.0
    """
    # The goal is to end up with a writable contiguous array to pass to Cython

    # First we check and make arrays.
    a1 = np.asarray_chkfinite(a) if check_finite else np.asarray(a)
    _deprecate_dtypes("linalg.det", a1)

    if a1.ndim < 2:
        raise ValueError('The input array must be at least two-dimensional.')
    if a1.shape[-1] != a1.shape[-2]:
        raise ValueError('Last 2 dimensions of the array must be square'
                         f' but received shape {a1.shape}.')

    # Also check if dtype is LAPACK compatible
    a1, overwrite_a = _normalize_lapack_dtype1(a1, overwrite_a)

    # Empty array has determinant 1 because math.
    if min(*a1.shape) == 0:
        dtyp = np.float64 if a1.dtype.char not in 'FD' else np.complex128
        if a1.ndim == 2:
            return dtyp(1.0)
        else:
            return np.ones(shape=a1.shape[:-2], dtype=dtyp)

    # Scalar case
    if a1.shape[-2:] == (1, 1):
        a1 = a1[..., 0, 0]
        if a1.ndim == 0:
            a1 = a1[()]
        # Convert float32 to float64, and complex64 to complex128.
        if a1.dtype.char in 'dD':
            return a1
        return a1.astype('d') if a1.dtype.char == 'f' else a1.astype('D')

    det = _linalg_det(a1, overwrite_a)

    # Promote single precision to double to prevent overflows
    # Cf. np.linalg.det(np.diag([1e+38, 1e+38]).astype(np.float32))
    if det.dtype.char == 'f':
        det = det.astype(np.float64)
    elif det.dtype.char == 'F':
        det = det.astype(np.complex128)

    # Return scalar for 2D input
    if det.ndim == 0:
        return det[()]
    return det


def det(a):
    """
    Compute the determinant of an array.

    Parameters
    ----------
    a : (..., M, M) array_like
        Input array to compute determinants for.

    Returns
    -------
    det : (...) array_like
        Determinant of `a`.

    See Also
    --------
    slogdet : Another way to represent the determinant, more suitable
      for large matrices where underflow/overflow may occur.
    scipy.linalg.det : Similar function in SciPy.

    Notes
    -----
    Broadcasting rules apply, see the `numpy.linalg` documentation for
    details.

    The determinant is computed via LU factorization using the LAPACK
    routine ``z/dgetrf``.

    Examples
    --------
    The determinant of a 2-D array [[a, b], [c, d]] is ad - bc:

    >>> import numpy as np
    >>> a = np.array([[1, 2], [3, 4]])
    >>> np.linalg.det(a)
    -2.0 # may vary

    Computing determinants for a stack of matrices:

    >>> a = np.array([ [[1, 2], [3, 4]], [[1, 2], [2, 1]], [[1, 3], [3, 1]] ])
    >>> a.shape
    (3, 2, 2)
    >>> np.linalg.det(a)
    array([-2., -3., -8.])

    """
    a = asarray(a)
    _assert_stacked_square(a)
    t, result_t = _commonType(a)
    signature = 'D->D' if isComplexType(t) else 'd->d'
    r = _umath_linalg.det(a, signature=signature)
    r = r.astype(result_t, copy=False)
    return r


def det(a: ArrayLike) -> Array:
  """
  Compute the determinant of an array.

  JAX implementation of :func:`numpy.linalg.det`.

  Args:
    a: array of shape ``(..., M, M)`` for which to compute the determinant.

  Returns:
    An array of determinants of shape ``a.shape[:-2]``.

  See also:
    :func:`jax.scipy.linalg.det`: Scipy-style API for determinant.

  Examples:
    >>> a = jnp.array([[1, 2],
    ...                [3, 4]])
    >>> jnp.linalg.det(a)
    Array(-2., dtype=float32)
  """
  a = ensure_arraylike("jnp.linalg.det", a)
  a, = promote_dtypes_inexact(a)
  a_shape = np.shape(a)
  if len(a_shape) >= 2 and a_shape[-1] == 2 and a_shape[-2] == 2:
    return _det_2x2(a)
  elif len(a_shape) >= 2 and a_shape[-1] == 3 and a_shape[-2] == 3:
    return _det_3x3(a)
  elif len(a_shape) >= 2 and a_shape[-1] == a_shape[-2]:
    return _det(a)
  else:
    msg = "Argument to _det() must have shape [..., n, n], got {}"
    raise ValueError(msg.format(a_shape))


def det(a: ArrayLike, overwrite_a: bool = False, check_finite: bool = True) -> Array:
  """Compute the determinant of a matrix

  JAX implementation of :func:`scipy.linalg.det`.

  Args:
    a: input array, of shape ``(..., N, N)``
    overwrite_a: unused by JAX
    check_finite: unused by JAX

  Returns
    Determinant of shape ``a.shape[:-2]``

  See Also:
    :func:`jax.numpy.linalg.det`: NumPy-style determinant API

  Examples:
    Determinant of a small 2D array:

    >>> x = jnp.array([[1., 2.],
    ...                [3., 4.]])
    >>> jax.scipy.linalg.det(x)
    Array(-2., dtype=float32)

    Batch-wise determinant of multiple 2D arrays:

    >>> x = jnp.array([[[1., 2.],
    ...                 [3., 4.]],
    ...                [[8., 5.],
    ...                 [7., 9.]]])
    >>> jax.scipy.linalg.det(x)
    Array([-2., 37.], dtype=float32)
  """
  del overwrite_a, check_finite  # unused
  return jnp_linalg.det(a)


def det(x: FloatArray['*d m m']) -> FloatArray['*d']:
  """Like `np.linalg.det` but auto-support jnp, tnp, np."""
  return _tf_or_xnp(x).linalg.det(x)

