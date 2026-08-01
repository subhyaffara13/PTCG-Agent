
def cho_factor(a, lower=False, overwrite_a=False, check_finite=True):
    """
    Compute the Cholesky decomposition of a matrix, to use in cho_solve.

    Returns a matrix containing the Cholesky decomposition,
    ``A = L L*`` or ``A = U* U`` of a Hermitian positive-definite matrix `a`.
    The return value can be directly used as the first parameter to cho_solve.

    .. warning::
        If `overwrite_a` is disabled, this function matches `cholesky` and
        zeros the other triangle. If it is enabled, the returned matrix may
        contain random data in the entries not used by the Cholesky
        decomposition, saving out on the explicit putting to 0 done by
        `cholesky`.

    Parameters
    ----------
    a : (..., M, M) array_like
        Matrix to be decomposed
    lower : bool, optional
        Whether to compute the upper or lower triangular Cholesky factorization.
        During decomposition, only the selected half of the matrix is referenced.
        (Default: upper-triangular)
    overwrite_a : bool, optional
        Whether to overwrite data in ``a`` (may improve performance). Default is False.
        See :ref:`tutorial_linalg_overwrite` for details.
    check_finite : bool, optional
        Whether to check that the entire input matrix contains only finite numbers.
        Disabling may give a performance gain, but may result in problems
        (crashes, non-termination) if the inputs do contain infinities or NaNs.

    Returns
    -------
    c : (..., M, M) ndarray
        Matrix whose upper or lower triangle contains the Cholesky factor
        of `a`. Other parts of the matrix contain random data.
    lower : ndarray, bool
        Flag indicating whether the factor is in the lower or upper triangle

    Raises
    ------
    LinAlgError
        Raised if decomposition fails.

    See Also
    --------
    cholesky : Compute the Cholesky decomposition and explicitly put the
                other triangle to 0.
    cho_solve : Solve a linear set equations using the Cholesky factorization
                of a matrix.

    Notes
    -----
    During the finiteness check (if selected), the entire matrix `a` is
    checked. During decomposition, `a` is assumed to be symmetric or Hermitian
    (as applicable), and only the half selected by option `lower` is referenced.
    Consequently, if `a` is asymmetric/non-Hermitian, `cholesky` may still
    succeed if the symmetric/Hermitian matrix represented by the selected half
    is positive definite, yet it may fail if an element in the other half is
    non-finite.

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.linalg import cho_factor
    >>> A = np.array([[9, 3, 1, 5], [3, 7, 5, 1], [1, 5, 9, 2], [5, 1, 2, 6]],
    ...             dtype=float, order="F")
    >>> A_ref = np.copy(A)
    >>> c, low = cho_factor(A)
    >>> c
    array([[3.        , 1.        , 0.33333333, 1.66666667],
           [0.        , 2.44948974, 1.90515869, -0.27216553],
           [0.        , 0.        , 2.29330749, 0.8559528 ],
           [0.        , 0.        , 0.        , 1.55418563]])
    >>> np.allclose(c.T @ c - A, np.zeros((4, 4)))
    True
    >>> c, low = cho_factor(A, overwrite_a=True)
    >>> c
    array([[3.        , 1.        , 0.33333333, 1.66666667],
           [3.        , 2.44948974, 1.90515869, -0.27216553],
           [1.        , 5.        , 2.29330749, 0.8559528 ],
           [5.        , 1.        , 2.        , 1.55418563]])
    >>> np.allclose(np.triu(c).T @ np.triu(c) - A_ref, np.zeros((4, 4)))
    True

    """
    # `clean=False` to represent that it is not necessary to set other triangle to 0.
    c = _cholesky(a, lower=lower, overwrite_a=overwrite_a, clean=False,
                    check_finite=check_finite)

    # broadcast `lower` argument for backwards compat
    batch_shape = a.shape[:-2]
    ret_lower = np.tile(lower, reps=batch_shape)

    return c, ret_lower


def cho_factor(a: ArrayLike, lower: bool = False, overwrite_a: bool = False,
               check_finite: bool = True) -> tuple[Array, bool]:
  """Factorization for Cholesky-based linear solves

  JAX implementation of :func:`scipy.linalg.cho_factor`. This function returns
  a result suitable for use with :func:`jax.scipy.linalg.cho_solve`. For direct
  Cholesky decompositions, prefer :func:`jax.scipy.linalg.cholesky`.

  Args:
    a: input array, representing a (batched) positive-definite hermitian matrix.
      Must have shape ``(..., N, N)``.
    lower: if True, compute the lower triangular Cholesky decomposition (default: False).
    overwrite_a: unused by JAX
    check_finite: unused by JAX

  Returns:
    ``(c, lower)``: ``c`` is an array of shape ``(..., N, N)`` representing the lower or
    upper cholesky decomposition of the input; ``lower`` is a boolean specifying whether
    this is the lower or upper decomposition.

  See Also:
    - :func:`jax.scipy.linalg.cholesky`
    - :func:`jax.scipy.linalg.cho_solve`

  Examples:
    A small real Hermitian positive-definite matrix:

    >>> x = jnp.array([[2., 1.],
    ...                [1., 2.]])

    Compute the cholesky factorization via :func:`~jax.scipy.linalg.cho_factor`,
    and use it to solve a linear equation via :func:`~jax.scipy.linalg.cho_solve`.

    >>> b = jnp.array([3., 4.])
    >>> cfac = jax.scipy.linalg.cho_factor(x)
    >>> y = jax.scipy.linalg.cho_solve(cfac, b)
    >>> y
    Array([0.6666666, 1.6666666], dtype=float32)

    Check that the result is consistent:

    >>> jnp.allclose(x @ y, b)
    Array(True, dtype=bool)
  """
  del overwrite_a, check_finite  # Unused
  return (cholesky(a, lower=lower), lower)

