
def lu(expr):
    return LofLU(expr), UofLU(expr)


def lu(a, permute_l=False, overwrite_a=False, check_finite=True,
       p_indices=False):
    """
    Compute LU decomposition of a matrix with partial pivoting.

    The decomposition satisfies::

        A = P @ L @ U

    where ``P`` is a permutation matrix, ``L`` lower triangular with unit
    diagonal elements, and ``U`` upper triangular. If `permute_l` is set to
    ``True`` then ``L`` is returned already permuted and hence satisfying
    ``A = L @ U``.

    Array argument(s) of this function may have additional
    "batch" dimensions prepended to the core shape. In this case, the array is treated
    as a batch of lower-dimensional slices; see :ref:`linalg_batch` for details.

    Parameters
    ----------
    a : (..., M, N) array_like
        Array to decompose
    permute_l : bool, optional
        Perform the multiplication P*L (Default: do not permute)
    overwrite_a : bool, optional
        Whether to overwrite data in a (may improve performance). Default is False.
        See :ref:`tutorial_linalg_overwrite` for details.
    check_finite : bool, optional
        Whether to check that the input matrix contains only finite numbers.
        Disabling may give a performance gain, but may result in problems
        (crashes, non-termination) if the inputs do contain infinities or NaNs.
    p_indices : bool, optional
        If ``True`` the permutation information is returned as row indices.
        The default is ``False`` for backwards-compatibility reasons.

    Returns
    -------
    (p, l, u) | (pl, u):
        The tuple `(p, l, u)` is returned if `permute_l` is ``False`` (default) else
        the tuple `(pl, u)` is returned, where:

        p : (..., M, M) ndarray
            Permutation arrays or vectors depending on `p_indices`.
        l : (..., M, K) ndarray
            Lower triangular or trapezoidal array with unit diagonal, where the last
            dimension is ``K = min(M, N)``.
        pl : (..., M, K) ndarray
            Permuted L matrix with last dimension being ``K = min(M, N)``.
        u : (..., K, N) ndarray
            Upper triangular or trapezoidal array.

    Notes
    -----
    Permutation matrices are costly since they are nothing but row reorder of
    ``L`` and hence indices are strongly recommended to be used instead if the
    permutation is required. The relation in the 2D case then becomes simply
    ``A = L[P, :] @ U``. In higher dimensions, it is better to use `permute_l`
    to avoid complicated indexing tricks.

    In 2D case, if one has the indices however, for some reason, the
    permutation matrix is still needed then it can be constructed by
    ``np.eye(M)[P, :]``.

    Examples
    --------

    >>> import numpy as np
    >>> from scipy.linalg import lu
    >>> A = np.array([[2, 5, 8, 7], [5, 2, 2, 8], [7, 5, 6, 6], [5, 4, 4, 8]])
    >>> p, l, u = lu(A)
    >>> np.allclose(A, p @ l @ u)
    True
    >>> p  # Permutation matrix
    array([[0., 1., 0., 0.],  # Row index 1
           [0., 0., 0., 1.],  # Row index 3
           [1., 0., 0., 0.],  # Row index 0
           [0., 0., 1., 0.]]) # Row index 2
    >>> p, _, _ = lu(A, p_indices=True)
    >>> p
    array([1, 3, 0, 2], dtype=int32)  # as given by row indices above
    >>> np.allclose(A, l[p, :] @ u)
    True

    We can also use nd-arrays, for example, a demonstration with 4D array:

    >>> rng = np.random.default_rng()
    >>> A = rng.uniform(low=-4, high=4, size=[3, 2, 4, 8])
    >>> p, l, u = lu(A)
    >>> p.shape, l.shape, u.shape
    ((3, 2, 4, 4), (3, 2, 4, 4), (3, 2, 4, 8))
    >>> np.allclose(A, p @ l @ u)
    True
    >>> PL, U = lu(A, permute_l=True)
    >>> np.allclose(A, PL @ U)
    True

    """
    a1 = np.asarray_chkfinite(a) if check_finite else np.asarray(a)
    _deprecate_dtypes("lu", a1)
    if a1.ndim < 2:
        raise ValueError('The input array must be at least two-dimensional.')

    # Also check if dtype is LAPACK compatible
    a1, overwrite_a = _normalize_lapack_dtype(a1, overwrite_a)

    *nd, m, n = a1.shape
    k = min(m, n)
    real_dchar = 'f' if a1.dtype.char in 'fF' else 'd'

    # Empty input
    if min(*a1.shape) == 0:
        if permute_l:
            PL = np.empty(shape=[*nd, m, k], dtype=a1.dtype)
            U = np.empty(shape=[*nd, k, n], dtype=a1.dtype)
            return PL, U
        else:
            P = (np.empty([*nd, 0], dtype=np.int32) if p_indices else
                 np.empty([*nd, 0, 0], dtype=real_dchar))
            L = np.empty(shape=[*nd, m, k], dtype=a1.dtype)
            U = np.empty(shape=[*nd, k, n], dtype=a1.dtype)
            return P, L, U

    # Scalar case
    if a1.shape[-2:] == (1, 1):
        if permute_l:
            return np.ones_like(a1), (a1 if overwrite_a else a1.copy())
        else:
            P = (np.zeros(shape=[*nd, m], dtype=int) if p_indices
                 else np.ones_like(a1))
            return P, np.ones_like(a1), (a1 if overwrite_a else a1.copy())

    P, L, U = _linalg_lu(a1, permute_l, overwrite_a)

    # Convert permutation vecs to permutation arrays
    # permute_l=False needed to enter here to avoid wasted efforts
    if (not p_indices) and (not permute_l):
        if nd:
            Pa = np.zeros([*nd, m, m], dtype=real_dchar)
            # An unreadable index hack - One-hot encoding for perm matrices
            nd_ix = np.ix_(*([np.arange(x) for x in nd]+[np.arange(m)]))
            Pa[(*nd_ix, P)] = 1
            P = Pa
        else:  # 2D case
            Pa = np.zeros([m, m], dtype=real_dchar)
            Pa[np.arange(m), P] = 1
            P = Pa

    return (L, U) if permute_l else (P, L, U)


def lu(x: ArrayLike) -> tuple[Array, Array, Array]:
  r"""LU decomposition with partial pivoting.

  Computes the matrix decomposition:

  .. math::
    P \, A = L \, U

  where :math:`P` is a permutation of the rows of :math:`A`, :math:`L` is a
  lower-triangular matrix with unit-diagonal elements, and :math:`U` is an
  upper-triangular matrix.

  Args:
    x: A batch of matrices with shape ``[..., m, n]``.

  Returns:
    A tuple ``(lu, pivots, permutation)``.

    ``lu`` is a batch of matrices with the same shape and dtype as ``x``
    containing the :math:`L` matrix in its lower triangle and the :math:`U`
    matrix in its upper triangle. The (unit) diagonal elements of :math:`L` are
    not represented explicitly.

    ``pivots`` is an int32 array with shape ``[..., min(m, n)]`` representing a
    sequence of row swaps that should be performed on :math:`A`.

    ``permutation`` is an alternative representation of the sequence of row
    swaps as a permutation, represented as an int32 array with shape
    ``[..., m]``.
  """
  return lu_p.bind(x)


def lu(a: ArrayLike, permute_l: Literal[False] = False, overwrite_a: bool = False,
       check_finite: bool = True) -> tuple[Array, Array, Array]: ...


def lu(a: ArrayLike, permute_l: Literal[True], overwrite_a: bool = False,
       check_finite: bool = True) -> tuple[Array, Array]: ...


def lu(a: ArrayLike, permute_l: bool = False, overwrite_a: bool = False,
       check_finite: bool = True) -> tuple[Array, Array] | tuple[Array, Array, Array]: ...


def lu(a: ArrayLike, permute_l: bool = False, overwrite_a: bool = False,
       check_finite: bool = True) -> tuple[Array, Array] | tuple[Array, Array, Array]:
  """Compute the LU decomposition

  JAX implementation of :func:`scipy.linalg.lu`.

  The LU decomposition of a matrix `A` is:

  .. math::

     A = P L U

  where `P` is a permutation matrix, `L` is lower-triangular and `U` is upper-triangular.

  Args:
    a: array of shape ``(..., M, N)`` to decompose.
    permute_l: if True, then permute ``L`` and return ``(P @ L, U)`` (default: False)
    overwrite_a: not used by JAX
    check_finite: not used by JAX

  Returns:
    A tuple of arrays ``(P @ L, U)`` if ``permute_l`` is True, else ``(P, L, U)``:

    - ``P`` is a permutation matrix of shape ``(..., M, M)``
    - ``L`` is a lower-triangular matrix of shape ``(... M, K)``
    - ``U`` is an upper-triangular matrix of shape ``(..., K, N)``

    with ``K = min(M, N)``

  See also:
    - :func:`jax.numpy.linalg.lu`: NumPy-style API for LU decomposition.
    - :func:`jax.lax.linalg.lu`: XLA-style API for LU decomposition.
    - :func:`jax.scipy.linalg.lu_solve`: LU-based linear solver.

  Examples:
    An LU decomposition of a 3x3 matrix:

    >>> a = jnp.array([[1., 2., 3.],
    ...                [5., 4., 2.],
    ...                [3., 2., 1.]])
    >>> P, L, U = jax.scipy.linalg.lu(a)

    ``P`` is a permutation matrix: i.e. each row and column has a single ``1``:

    >>> P
    Array([[0., 1., 0.],
           [1., 0., 0.],
           [0., 0., 1.]], dtype=float32)

    ``L`` and ``U`` are lower-triangular and upper-triangular matrices:

    >>> with jnp.printoptions(precision=3):
    ...   print(L)
    ...   print(U)
    [[ 1.     0.     0.   ]
     [ 0.2    1.     0.   ]
     [ 0.6   -0.333  1.   ]]
    [[5.    4.    2.   ]
     [0.    1.2   2.6  ]
     [0.    0.    0.667]]

    The original matrix can be reconstructed by multiplying the three together:

    >>> a_reconstructed = P @ L @ U
    >>> jnp.allclose(a, a_reconstructed)
    Array(True, dtype=bool)
  """
  del overwrite_a, check_finite  # unused
  return _lu(a, permute_l)

