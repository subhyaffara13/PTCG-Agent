
def lu_solve(lu_and_piv, b, trans=0, overwrite_b=False, check_finite=True):
    """Solve an equation system, ``a @ x = b``, given the LU factorization of a.

    The documentation is written assuming array arguments are of specified
    "core" shapes. However, array argument(s) of this function may have additional
    "batch" dimensions prepended to the core shape. In this case, the array is treated
    as a batch of lower-dimensional slices; see :ref:`linalg_batch` for details.

    Parameters
    ----------
    lu_and_piv : tuple
        Factorization of the coefficient matrix a in the form ``(lu, piv)``, as given
        by lu_factor. In particular piv are 0-indexed pivot indices.
    b : array
        Right-hand side
    trans : {0, 1, 2}, optional
        Type of system to solve:

        =====  =========
        trans  system
        =====  =========
        0      a x   = b
        1      a^T x = b
        2      a^H x = b
        =====  =========
    overwrite_b : bool, optional
        Whether to overwrite data in b (may increase performance)
        See :ref:`tutorial_linalg_overwrite` for details.
    check_finite : bool, optional
        Whether to check that the input matrices contain only finite numbers.
        Disabling may give a performance gain, but may result in problems
        (crashes, non-termination) if the inputs do contain infinities or NaNs.

    Returns
    -------
    x : array
        Solution to the system

    See Also
    --------
    lu_factor : LU factorize a matrix

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.linalg import lu_factor, lu_solve
    >>> A = np.array([[2, 5, 8, 7], [5, 2, 2, 8], [7, 5, 6, 6], [5, 4, 4, 8]])
    >>> b = np.array([1, 1, 1, 1])
    >>> lu, piv = lu_factor(A)
    >>> x = lu_solve((lu, piv), b)
    >>> np.allclose(A @ x - b, np.zeros((4,)))
    True

    """
    (lu, piv) = lu_and_piv
    return _lu_solve(lu, piv, b, trans=trans, overwrite_b=overwrite_b,
                     check_finite=check_finite)


def lu_solve(lu: ArrayLike, permutation: ArrayLike, b: ArrayLike,
             trans: int = 0) -> Array:
  """LU solve with broadcasting."""
  return _lu_solve(lu, permutation, b, trans)


def lu_solve(lu_and_piv: tuple[Array, ArrayLike], b: ArrayLike, trans: int = 0,
             overwrite_b: bool = False, check_finite: bool = True) -> Array:
  """Solve a linear system using an LU factorization

  JAX implementation of :func:`scipy.linalg.lu_solve`. Uses the output
  of :func:`jax.scipy.linalg.lu_factor`.

  Args:
    lu_and_piv: ``(lu, piv)``, output of :func:`~jax.scipy.linalg.lu_factor`.
      ``lu`` is an array of shape ``(..., M, N)``, containing ``L`` in its lower
      triangle and ``U`` in its upper. ``piv`` is an array of shape ``(..., K)``,
      with ``K = min(M, N)``, which encodes the pivots.
    b: right-hand-side of linear system. Array of shape ``(M,)`` (for a
      1-dimensional right-hand-side) or ``(..., M, K)`` (for a batched
      2-dimensional right-hand-side).
    trans: type of system to solve. Options are:

      - ``0``: :math:`A x = b`
      - ``1``: :math:`A^Tx = b`
      - ``2``: :math:`A^Hx = b`

    overwrite_b: unused by JAX
    check_finite: unused by JAX

  Returns:
    Array representing the solution of the linear system. The result has
    shape ``(..., N)`` if ``b`` is of shape ``(M,)``, and has shape
    ``(..., N, K)`` otherwise.

  See Also:
    - :func:`jax.scipy.linalg.lu`
    - :func:`jax.scipy.linalg.lu_factor`

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
  del overwrite_b, check_finite  # unused
  lu, pivots = lu_and_piv
  lu, b = promote_dtypes_inexact(jnp.asarray(lu), jnp.asarray(b))
  m, _ = lu.shape[-2:]
  perm = lax_linalg.lu_pivots_to_permutation(pivots, m)
  if b.ndim == 1:
    signature = "(n,n),(n),(n)->(n)"
  elif lu.ndim == b.ndim + 1 and lu.shape[-1] == b.shape[-1]:
    # Deprecation warning added 2026-03-23
    warnings.warn(
        "jax.scipy.linalg.lu_solve: batched 1D solves with b.ndim > 1 are "
        "deprecated, and in the future will be treated as a batched 2D solve. "
        "Use lu_solve(lu_and_piv, b[..., None]).squeeze(-1) to avoid this warning.",
        category=FutureWarning)
    signature = "(n,n),(n),(n)->(n)"
  else:
    signature = "(n,n),(n),(n,k)->(n,k)"
  return jnp_vectorize.vectorize(
      partial(lax_linalg.lu_solve, trans=trans),
      signature=signature)(lu, perm, b)

