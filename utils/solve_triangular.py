from typing import Any

def solve_triangular(a, b, trans=0, lower=False, unit_diagonal=False,
                     overwrite_b=False, check_finite=True):
    """
    Solve the equation ``a @ x = b`` for ``x``, where `a` is a triangular matrix.

    Parameters
    ----------
    a : (M, M) array_like
        A triangular matrix
    b : (M,) or (M, N) array_like
        Right-hand side matrix in ``a x = b``
    trans : {0, 1, 2, 'N', 'T', 'C'}, optional
        Type of system to solve:

        ========  =========
        trans     system
        ========  =========
        0 or 'N'  a x  = b
        1 or 'T'  a^T x = b
        2 or 'C'  a^H x = b
        ========  =========
    lower : bool, optional
        Use only data contained in the lower triangle of `a`.
        Default is to use upper triangle.
    unit_diagonal : bool, optional
        If True, diagonal elements of `a` are assumed to be 1 and
        will not be referenced.
    overwrite_b : bool, optional
        Allow overwriting data in `b` (may enhance performance)
        See :ref:`tutorial_linalg_overwrite` for details.
    check_finite : bool, optional
        Whether to check that the input matrices contain only finite numbers.
        Disabling may give a performance gain, but may result in problems
        (crashes, non-termination) if the inputs do contain infinities or NaNs.

    Returns
    -------
    x : (M,) or (M, N) ndarray
        Solution to the system ``a x = b``.  Shape of return matches `b`.

    Raises
    ------
    LinAlgError
        If `a` is singular

    Notes
    -----
    .. versionadded:: 0.9.0

    Examples
    --------
    Solve the lower triangular system a x = b, where::

             [3  0  0  0]       [4]
        a =  [2  1  0  0]   b = [2]
             [1  0  1  0]       [4]
             [1  1  1  1]       [2]

    >>> import numpy as np
    >>> from scipy.linalg import solve_triangular
    >>> a = np.array([[3, 0, 0, 0], [2, 1, 0, 0], [1, 0, 1, 0], [1, 1, 1, 1]])
    >>> b = np.array([4, 2, 4, 2])
    >>> x = solve_triangular(a, b, lower=True)
    >>> x
    array([ 1.33333333, -0.66666667,  2.66666667, -1.33333333])
    >>> a.dot(x)  # Check the result
    array([ 4.,  2.,  4.,  2.])

    """

    a1 = _asarray_validated(a, check_finite=check_finite)
    b1 = _asarray_validated(b, check_finite=check_finite)

    if len(a1.shape) != 2 or a1.shape[0] != a1.shape[1]:
        raise ValueError('expected square matrix')

    if a1.shape[0] != b1.shape[0]:
        raise ValueError(f'shapes of a {a1.shape} and b {b1.shape} are incompatible')

    # accommodate empty arrays
    if b1.size == 0:
        dt_nonempty = solve_triangular(
            np.eye(2, dtype=a1.dtype), np.ones(2, dtype=b1.dtype)
        ).dtype
        return np.empty_like(b1, dtype=dt_nonempty)

    overwrite_b = overwrite_b or _datacopied(b1, b)

    x, _ = _solve_triangular(a1, b1, trans, lower, unit_diagonal, overwrite_b)
    return x


def solve_triangular(a: ArrayLike, b: ArrayLike, trans: int | str = 0, lower: bool = False,
                     unit_diagonal: bool = False, overwrite_b: bool = False,
                     debug: Any = None, check_finite: bool = True) -> Array:
  """Solve a triangular linear system of equations

  JAX implementation of :func:`scipy.linalg.solve_triangular`.

  This solves a (batched) linear system of equations ``a @ x = b`` for ``x``
  given a triangular matrix ``a`` and a vector or matrix ``b``.

  Args:
    a: array of shape ``(..., N, N)``. Only part of the array will be accessed,
      depending on the ``lower`` and ``unit_diagonal`` arguments.
    b: array of shape ``(N,)`` (for a 1-dimensional right-hand-side) or
      ``(..., N, M)`` (for a batched 2-dimensional right-hand-side).
    lower: If True, only use the lower triangle of the input, If False (default),
      only use the upper triangle.
    unit_diagonal: If True, ignore diagonal elements of ``a`` and assume they are
      ``1`` (default: False).
    trans: specify what properties of ``a`` can be assumed. Options are:

      - ``0`` or ``'N'``: solve :math:`Ax=b`
      - ``1`` or ``'T'``: solve :math:`A^Tx=b`
      - ``2`` or ``'C'``: solve :math:`A^Hx=b`

    overwrite_b: unused by JAX
    debug: unused by JAX
    check_finite: unused by JAX

  Returns:
    An array containing the solution to the linear system. The result has
    shape ``(..., N)`` if ``b`` is of shape ``(N,)``, and has shape
    ``(..., N, M)`` otherwise.

  See also:
    :func:`jax.scipy.linalg.solve`: Solve a general linear system.

  Examples:
    A simple 3x3 triangular linear system:

    >>> A = jnp.array([[1., 2., 3.],
    ...                [0., 3., 2.],
    ...                [0., 0., 5.]])
    >>> b = jnp.array([10., 8., 5.])
    >>> x = jax.scipy.linalg.solve_triangular(A, b)
    >>> x
    Array([3., 2., 1.], dtype=float32)

    Confirming that the result solves the system:

    >>> jnp.allclose(A @ x, b)
    Array(True, dtype=bool)

    Computing the transposed problem:

    >>> x = jax.scipy.linalg.solve_triangular(A, b, trans='T')
    >>> x
    Array([10. , -4. , -3.4], dtype=float32)

    Confirming that the result solves the system:

    >>> jnp.allclose(A.T @ x, b)
    Array(True, dtype=bool)
  """
  del overwrite_b, debug, check_finite  # unused
  return _solve_triangular(a, b, trans, lower, unit_diagonal)

