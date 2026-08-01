
def fiedler(a):
    """Returns a symmetric Fiedler matrix.

    Given an sequence of numbers `a`, Fiedler matrices have the structure
    ``F[i, j] = np.abs(a[i] - a[j])``, and hence zero diagonals and nonnegative
    entries. A Fiedler matrix has a dominant positive eigenvalue and other
    eigenvalues are negative. Although not valid generally, for certain inputs,
    the inverse and the determinant can be derived explicitly as given in [1]_.

    Array argument(s) of this function may have additional
    "batch" dimensions prepended to the core shape. In this case, the array is treated
    as a batch of lower-dimensional slices; see :ref:`linalg_batch` for details.

    Parameters
    ----------
    a : (..., n,) array_like
        Coefficient array. N-dimensional arrays are treated as a batch:
        each slice along the last axis is a 1-D coefficient array.

    Returns
    -------
    F : (..., n, n) ndarray
        Fiedler matrix. For batch input, each slice of shape ``(n, n)``
        along the last two dimensions of the output corresponds with a
        slice of shape ``(n,)`` along the last dimension of the input.

    See Also
    --------
    circulant, toeplitz

    Notes
    -----

    .. versionadded:: 1.3.0

    References
    ----------
    .. [1] J. Todd, "Basic Numerical Mathematics: Vol.2 : Numerical Algebra",
        1977, Birkhauser, :doi:`10.1007/978-3-0348-7286-7`

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.linalg import det, inv, fiedler
    >>> a = [1, 4, 12, 45, 77]
    >>> n = len(a)
    >>> A = fiedler(a)
    >>> A
    array([[ 0,  3, 11, 44, 76],
           [ 3,  0,  8, 41, 73],
           [11,  8,  0, 33, 65],
           [44, 41, 33,  0, 32],
           [76, 73, 65, 32,  0]])

    The explicit formulas for determinant and inverse seem to hold only for
    monotonically increasing/decreasing arrays. Note the tridiagonal structure
    and the corners.

    >>> Ai = inv(A)
    >>> Ai[np.abs(Ai) < 1e-12] = 0.  # cleanup the numerical noise for display
    >>> Ai
    array([[-0.16008772,  0.16666667,  0.        ,  0.        ,  0.00657895],
           [ 0.16666667, -0.22916667,  0.0625    ,  0.        ,  0.        ],
           [ 0.        ,  0.0625    , -0.07765152,  0.01515152,  0.        ],
           [ 0.        ,  0.        ,  0.01515152, -0.03077652,  0.015625  ],
           [ 0.00657895,  0.        ,  0.        ,  0.015625  , -0.00904605]])
    >>> det(A)
    15409151.999999998
    >>> (-1)**(n-1) * 2**(n-2) * np.diff(a).prod() * (a[-1] - a[0])
    15409152

    """
    xp = array_namespace(a)
    a = xpx.atleast_nd(xp.asarray(a), ndim=1)

    if xp_size(a) == 0:
        return xp.empty((0, 0), dtype=xp.float64)
    elif xp_size(a) == 1:
        return xp.asarray([[0.]])
    else:
        return xp.abs(a[..., :, xp.newaxis] - a[..., xp.newaxis, :])


def fiedler(a: ArrayLike) -> Array:
  r"""Construct a symmetric Fiedler matrix.

  JAX implementation of :func:`scipy.linalg.fiedler`.

  The Fiedler matrix has entries :math:`F_{ij} = |a_i - a_j|` for
  :math:`0 \le i, j < n`, where ``a`` is the input vector. The result is
  symmetric with a zero diagonal.

  Args:
    a: array of shape ``(..., N)``.

  Returns:
    A Fiedler matrix of shape ``(..., N, N)``.

  Examples:
    >>> jax.scipy.linalg.fiedler(jnp.array([1, 4, 12, 45, 77]))
    Array([[ 0,  3, 11, 44, 76],
           [ 3,  0,  8, 41, 73],
           [11,  8,  0, 33, 65],
           [44, 41, 33,  0, 32],
           [76, 73, 65, 32,  0]], dtype=int32)
  """
  check_arraylike("fiedler", a)
  arr = jnp.atleast_1d(a)
  return jnp.abs(arr[..., None] - arr[..., None, :])

