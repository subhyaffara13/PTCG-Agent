
def cho_solve(c_and_lower, b, overwrite_b=False, check_finite=True):
    """Solve the linear equations A x = b, given the Cholesky factorization of A.

    The documentation is written assuming array arguments are of specified
    "core" shapes. However, array argument(s) of this function may have additional
    "batch" dimensions prepended to the core shape. In this case, the array is treated
    as a batch of lower-dimensional slices; see :ref:`linalg_batch` for details.

    Parameters
    ----------
    c_and_lower : tuple, (array, bool)
        Cholesky factorization of an array, as given by cho_factor.
        The first element of the
        tuple is the matrix containing the Cholesky factor, and the second element is a
        boolean flag indicating whether the factor is in the lower or upper triangle.
    b : array
        Right-hand side
    overwrite_b : bool, optional
        Whether to overwrite data in b (may improve performance)
        See :ref:`tutorial_linalg_overwrite` for details.
    check_finite : bool, optional
        Whether to check that the input matrices contain only finite numbers.
        Disabling may give a performance gain, but may result in problems
        (crashes, non-termination) if the inputs do contain infinities or NaNs.

    Returns
    -------
    x : array
        The solution to the system A x = b

    See Also
    --------
    cho_factor : Cholesky factorization of a matrix

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.linalg import cho_factor, cho_solve
    >>> A = np.array([[9, 3, 1, 5], [3, 7, 5, 1], [1, 5, 9, 2], [5, 1, 2, 6]])
    >>> c, low = cho_factor(A)
    >>> x = cho_solve((c, low), [1, 1, 1, 1])
    >>> np.allclose(A @ x - [1, 1, 1, 1], np.zeros(4))
    True

    """
    c, lower = c_and_lower
    return _cho_solve(c, b, lower, overwrite_b=overwrite_b, check_finite=check_finite)


def cho_solve(c_and_lower: tuple[ArrayLike, bool], b: ArrayLike,
              overwrite_b: bool = False, check_finite: bool = True) -> Array:
  """Solve a linear system using a Cholesky factorization

  JAX implementation of :func:`scipy.linalg.cho_solve`. Uses the output
  of :func:`jax.scipy.linalg.cho_factor`.

  Args:
    c_and_lower: ``(c, lower)``, where ``c`` is an array of shape ``(..., N, N)``
      representing the lower or upper cholesky decomposition of the matrix, and
      ``lower`` is a boolean specifying whether this is the lower or upper decomposition.
    b: right-hand-side of linear system. Array of shape ``(N,)`` (for a
      1-dimensional right-hand-side) or ``(..., N, M)`` (for a batched
      2-dimensional right-hand-side).
    overwrite_a: unused by JAX
    check_finite: unused by JAX

  Returns:
    Array representing the solution of the linear system. The result has
    shape ``(..., N)`` if ``b`` is of shape ``(N,)``, and has shape
    ``(..., N, M)`` otherwise.

  See Also:
    - :func:`jax.scipy.linalg.cholesky`
    - :func:`jax.scipy.linalg.cho_factor`

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
  del overwrite_b, check_finite  # Unused
  c, lower = c_and_lower
  return _cho_solve(c, b, lower)

