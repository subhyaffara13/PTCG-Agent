
def lu_factor(a, overwrite_a=False, check_finite=True):
    """
    Compute pivoted LU decomposition of a matrix.

    The decomposition is::

        A = P L U

    where P is a permutation matrix, L lower triangular with unit
    diagonal elements, and U upper triangular.

    Parameters
    ----------
    a : (M, N) array_like
        Matrix to decompose
    overwrite_a : bool, optional
        Whether to overwrite data in ``a`` (may improve performance). Default is False.
        See :ref:`tutorial_linalg_overwrite` for details.
    check_finite : bool, optional
        Whether to check that the input matrix contains only finite numbers.
        Disabling may give a performance gain, but may result in problems
        (crashes, non-termination) if the inputs do contain infinities or NaNs.

    Returns
    -------
    lu : (M, N) ndarray
        Matrix containing U in its upper triangle, and L in its lower triangle.
        The unit diagonal elements of L are not stored.
    piv : (K,) ndarray
        Pivot indices representing the permutation matrix P:
        row i of matrix was interchanged with row piv[i].
        Of shape ``(K,)``, with ``K = min(M, N)``.

    See Also
    --------
    lu : gives lu factorization in more user-friendly format
    lu_solve : solve an equation system using the LU factorization of a matrix

    Notes
    -----
    This is a wrapper to the ``*GETRF`` routines from LAPACK. Unlike
    :func:`lu`, it outputs the L and U factors into a single array
    and returns pivot indices instead of a permutation matrix.

    While the underlying ``*GETRF`` routines return 1-based pivot indices, the
    ``piv`` array returned by ``lu_factor`` contains 0-based indices.

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.linalg import lu_factor
    >>> A = np.array([[2, 5, 8, 7], [5, 2, 2, 8], [7, 5, 6, 6], [5, 4, 4, 8]])
    >>> lu, piv = lu_factor(A)
    >>> piv
    array([2, 2, 3, 3], dtype=int32)

    Convert LAPACK's ``piv`` array to NumPy index and test the permutation

    >>> def pivot_to_permutation(piv):
    ...     perm = np.arange(len(piv))
    ...     for i in range(len(piv)):
    ...         perm[i], perm[piv[i]] = perm[piv[i]], perm[i]
    ...     return perm
    ...
    >>> p_inv = pivot_to_permutation(piv)
    >>> p_inv
    array([2, 0, 3, 1])
    >>> L, U = np.tril(lu, k=-1) + np.eye(4), np.triu(lu)
    >>> np.allclose(A[p_inv] - L @ U, np.zeros((4, 4)))
    True

    The P matrix in P L U is defined by the inverse permutation and
    can be recovered using argsort:

    >>> p = np.argsort(p_inv)
    >>> p
    array([1, 3, 0, 2])
    >>> np.allclose(A - L[p] @ U, np.zeros((4, 4)))
    True

    or alternatively:

    >>> P = np.eye(4)[p]
    >>> np.allclose(A - P @ L @ U, np.zeros((4, 4)))
    True
    """
    if check_finite:
        a1 = asarray_chkfinite(a)
    else:
        a1 = asarray(a)

    # accommodate empty arrays
    if a1.size == 0:
        lu = np.empty_like(a1)
        piv = np.arange(0, dtype=np.int64 if HAS_ILP64 else np.int32)
        return lu, piv

    overwrite_a = overwrite_a or (_datacopied(a1, a))

    getrf, = get_lapack_funcs(('getrf',), (a1,))
    lu, piv, info = getrf(a1, overwrite_a=overwrite_a)
    if info < 0:
        raise ValueError(
            f'illegal value in {-info}th argument of internal getrf (lu_factor)'
        )
    if info > 0:
        warn(
            f"Diagonal number {info} is exactly zero. Singular matrix.",
            LinAlgWarning,
            stacklevel=2
        )
    return lu, piv


def lu_factor(a: ArrayLike, overwrite_a: bool = False, check_finite: bool = True) -> tuple[Array, Array]:
  """Factorization for LU-based linear solves

  JAX implementation of :func:`scipy.linalg.lu_factor`.

  This function returns a result suitable for use with :func:`jax.scipy.linalg.lu_solve`.
  For direct LU decompositions, prefer :func:`jax.scipy.linalg.lu`.

  Args:
    a: input array of shape ``(..., M, N)``.
    overwrite_a: unused by JAX
    check_finite: unused by JAX

  Returns:
    A tuple ``(lu, piv)``

    - ``lu`` is an array of shape ``(..., M, N)``, containing ``L`` in its
      lower triangle and ``U`` in its upper.
    - ``piv`` is an array of shape ``(..., K)`` with ``K = min(M, N)``,
      which encodes the pivots.

  See Also:
    - :func:`jax.scipy.linalg.lu`
    - :func:`jax.scipy.linalg.lu_solve`

  Examples:
    Solving a small linear system via LU factorization:

    >>> a = jnp.array([[2., 1.],
    ...                [1., 2.]])

    Compute the lu factorization via :func:`~jax.scipy.linalg.lu_factor`,
    and use it to solve a linear equation via :func:`~jax.scipy.linalg.lu_solve`.

    >>> b = jnp.array([3., 4.])
    >>> lufac = jax.scipy.linalg.lu_factor(a)
    >>> y = jax.scipy.linalg.lu_solve(lufac, b)
    >>> y
    Array([0.6666666, 1.6666667], dtype=float32)

    Check that the result is consistent:

    >>> jnp.allclose(a @ y, b)
    Array(True, dtype=bool)
  """
  del overwrite_a, check_finite  # unused
  a, = promote_dtypes_inexact(jnp.asarray(a))
  lu, pivots, _ = lax_linalg.lu(a)
  return lu, pivots

