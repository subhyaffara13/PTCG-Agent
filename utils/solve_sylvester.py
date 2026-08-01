
def solve_sylvester(a, b, q):
    """
    Computes a solution (X) to the Sylvester equation :math:`AX + XB = Q`.

    Parameters
    ----------
    a : (M, M) array_like
        Leading matrix of the Sylvester equation
    b : (N, N) array_like
        Trailing matrix of the Sylvester equation
    q : (M, N) array_like
        Right-hand side

    Returns
    -------
    x : (M, N) ndarray
        The solution to the Sylvester equation.

    Raises
    ------
    LinAlgError
        If solution was not found

    Notes
    -----
    Computes a solution to the Sylvester matrix equation via the Bartels-
    Stewart algorithm. The A and B matrices first undergo Schur
    decompositions. The resulting matrices are used to construct an
    alternative Sylvester equation (``RY + YS^T = F``) where the R and S
    matrices are in quasi-triangular form (or, when R, S or F are complex,
    triangular form). The simplified equation is then solved using
    ``*TRSYL`` from LAPACK directly.

    .. versionadded:: 0.11.0

    Examples
    --------
    Given `a`, `b`, and `q` solve for `x`:

    >>> import numpy as np
    >>> from scipy import linalg
    >>> a = np.array([[-3, -2, 0], [-1, -1, 3], [3, -5, -1]])
    >>> b = np.array([[1]])
    >>> q = np.array([[1],[2],[3]])
    >>> x = linalg.solve_sylvester(a, b, q)
    >>> x
    array([[ 0.0625],
           [-0.5625],
           [ 0.6875]])
    >>> np.allclose(a.dot(x) + x.dot(b), q)
    True

    """
    # Accommodate empty a
    if a.size == 0 or b.size == 0:
        tdict = {'s': np.float32, 'd': np.float64,
                 'c': np.complex64, 'z': np.complex128}
        func, = get_lapack_funcs(('trsyl',), arrays=(a, b, q))
        return np.empty(q.shape, dtype=tdict[func.typecode])

    # Compute the Schur decomposition form of a
    r, u = schur(a, output='real')

    # Compute the Schur decomposition of b
    s, v = schur(b.conj().transpose(), output='real')

    # Construct f = u'*q*v
    f = np.dot(np.dot(u.conj().transpose(), q), v)

    # Call the Sylvester equation solver
    trsyl, = get_lapack_funcs(('trsyl',), (r, s, f))
    if trsyl is None:
        raise RuntimeError('LAPACK implementation does not contain a proper '
                           'Sylvester equation solver (TRSYL)')
    y, scale, info = trsyl(r, s, f, tranb='C')

    y = scale*y

    if info < 0:
        raise LinAlgError(f"Illegal value encountered in the {-info} term")

    return np.dot(np.dot(u, y), v.conj().transpose())


def solve_sylvester(A: ArrayLike, B: ArrayLike, C: ArrayLike, *, method: str = "schur", tol: float = 1e-8) -> Array:
  """
  Solves the Sylvester equation
  .. math::

    AX + XB = C

  Using one of two methods.

  (1) Bartell-Stewart (schur) algorithm (default) [CPU ONLY]:

  Where A and B are first decomposed using Schur decomposition to construct and alternate sylvester equation:
  .. math::

    RY + YS^T = F

  Where R and S are in quasitriangular form when A and B are real valued and triangular when A and B are complex.

  (2) The Eigen decomposition algorithm [CPU and GPU]

  Args:
    A: array of shape ``(..., m, m)``
    B: array of shape ``(..., n, n)``
    C: array of shape ``(..., m, n)``. Batch dimensions are broadcast across
      ``A``, ``B``, and ``C``.
    method: "schur" is the default and is accurate but slow, and "eigen" is an alternative that is faster but less accurate for ill-conditioned matrices.
    tol: How close the sum of the eigenvalues from A and B can be to zero before returning matrix of NaNs

  Returns:
    Array of shape ``(..., m, n)`` representing the solution ``X``.

  Examples:
    >>> A = jax.numpy.array([[1, 2], [3, 4]])
    >>> B = jax.numpy.array([[5, 6], [7, 8]])
    >>> C = jax.numpy.array([[6, 8], [10, 12]])
    >>> X = jax.scipy.linalg.solve_sylvester(A, B, C)
    >>> print(X) # doctest: +SKIP
    [[1. 0.]
     [0.  1.]]

  Notes:
    The Bartel-Stewart algorithm is robust because a Schur decomposition always exists even for defective matrices,
    and it handles complex and ill-conditioned problems better than the eigen decomposition method.
    However, there are a couple of drawbacks. First, It is computationally more expensive than
    the eigen decomposition method because you need to perform a Schur decomposition and then scan the entire solution matrix.
    Second, it requires more system memory compared to the eigen decomposition method.

    The eigen decomposition method is the fastest method to solve a sylvester equation. However, this speed brings with it a couple of drawbacks.
    First, A and B must be diagonalizable otherwise the eigenvectors will be linearly dependent and ill-conditioned leading to accuracy issues.
    Second, when the eigenvectors are not orthogonal roundoff errors are amplified.

    Additionally, for complex types as the size of the matrix increases the accuracy of the results degrades. Float64 types are most robust to degradation.

    The tol argument allows you to specify how ill-conditioned a matrix can be and still estimate a solution.
    For matrices that are ill-conditioned we recommend using float64 instead of the default float32 dtype. The solver
    can still return good estimates for ill-conditioned matrices depending on how close to zero the sums of the eigenvalues of A and B
    are.
  """
  A, B, C = promote_dtypes_inexact(jnp.asarray(A), jnp.asarray(B), jnp.asarray(C))

  m, n = C.shape[-2:]
  if A.shape[-2:] != (m, m) or B.shape[-2:] != (n, n):
    raise ValueError(f"Incompatible shapes for Sylvester equation:\nA: {A.shape}\nB: {B.shape}\nC: {C.shape}")

  return jnp_vectorize.vectorize(
      partial(_solve_sylvester_2d, method=method, tol=tol),
      signature="(m,m),(n,n),(m,n)->(m,n)")(A, B, C)

