
def nnls(A, b, *, maxiter=None):
    """
    Solve ``argmin_x || Ax - b ||_2^2`` for ``x>=0``.

    This problem, often called as NonNegative Least Squares, is a convex
    optimization problem with convex constraints. It typically arises when
    the ``x`` models quantities for which only nonnegative values are
    attainable; weight of ingredients, component costs and so on.

    Parameters
    ----------
    A : (m, n) ndarray
        Coefficient array
    b : (m,) ndarray, float
        Right-hand side vector.
    maxiter : int, optional
        Maximum number of iterations, optional. Default value is ``3 * n``.

    Returns
    -------
    x : ndarray
        Solution vector.
    rnorm : float
        The 2-norm of the residual, ``|| Ax-b ||_2``.

    See Also
    --------
    lsq_linear : Linear least squares with bounds on the variables

    Notes
    -----
    The code is based on the classical algorithm of [1]_. It utilizes an active
    set method and solves the KKT (Karush-Kuhn-Tucker) conditions for the
    non-negative least squares problem.

    References
    ----------
    .. [1] : Lawson C., Hanson R.J., "Solving Least Squares Problems", SIAM,
       1995, :doi:`10.1137/1.9781611971217`

     Examples
    --------
    >>> import numpy as np
    >>> from scipy.optimize import nnls
    ...
    >>> A = np.array([[1, 0], [1, 0], [0, 1]])
    >>> b = np.array([2, 1, 1])
    >>> nnls(A, b)
    (array([1.5, 1. ]), 0.7071067811865475)

    >>> b = np.array([-1, -1, -1])
    >>> nnls(A, b)
    (array([0., 0.]), 1.7320508075688772)

    """

    A = np.asarray_chkfinite(A, dtype=np.float64, order='C')
    b = np.asarray_chkfinite(b, dtype=np.float64)

    if len(A.shape) != 2:
        raise ValueError(f"Expected a 2D array, but the shape of A is {A.shape}")

    if (b.ndim > 2) or ((b.ndim == 2) and (b.shape[1] != 1)):
        raise ValueError("Expected a 1D array,(or 2D with one column), but the,"
                         f" shape of b is {b.shape}")
    elif (b.ndim == 2) and (b.shape[1] == 1):
        b = b.ravel()

    m, n = A.shape

    if m != b.shape[0]:
        raise ValueError(
                "Incompatible dimensions. The first dimension of " +
                f"A is {m}, while the shape of b is {(b.shape[0], )}")

    if n == 0:
        return (np.empty(0), np.linalg.norm(b))

    if not maxiter:
        maxiter = 3*n
    x, rnorm, info = _nnls(A, b, maxiter)
    if info == 3:
        raise RuntimeError("Maximum number of iterations reached.")

    return x, rnorm


def nnls(
    A: jax.Array,
    b: jax.Array,
    iters: int,
    unroll: Union[int, bool] = 1,
    L: Union[jax.typing.ArrayLike, None] = None,
) -> jax.Array:
  r"""Solves the non-negative least squares problem.

  Minimizes :math:`\|A x - b\|_2` subject to :math:`x \geq 0`.

  Uses the fast projected gradient (FPG) algorithm of Polyak 2015.

  Args:
    A: Input matrix of shape `(M, N)`.
    b: Input vector of shape `(M,)` or matrix of shape `(M, K)`.
    iters: Number of iterations to run the algorithm for.
    unroll: Unroll parameter passed to `lax.scan`.
    L: An upper bound on the spectral radius of `A.mT @ A` (optional).

  Returns:
    A solution vector of shape `(N,)` or matrix of shape `(N, K)`.

  Examples:
    >>> from jax import numpy as jnp
    >>> import optax
    >>> A = jnp.array([[1., 2.], [3., 4.]])
    >>> b = jnp.array([5., 6.])
    >>> x = optax.nnls(A, b, 10**3)
    >>> print(f"{x[0]:.2f}")
    0.00
    >>> print(f"{x[1]:.2f}")
    1.70

  References:
    Roman A. Polyak, `Projected gradient method for non-negative least square
    <http://www.ams.org/books/conm/636/>`_, 2015
  """
  assert A.ndim == 2
  assert b.ndim in (1, 2)
  assert b.shape[0] == A.shape[0]

  Q = A.mT @ A
  q = A.mT @ b

  if L is None:
    L = get_spectral_radius_upper_bound(Q)

  L = jnp.where(L == 0, 1, L)  # avoid division by zero below

  def f(x_p_c, _):
    x, p, c = x_p_c

    cn = (1 + jnp.sqrt(1 + 4 * c ** 2)) / 2
    s = (c - 1) / cn

    xn = (p - (Q @ p - q) / L).clip(0)
    pn = xn + s * (xn - x)

    return (xn, pn, cn), None

  x = jnp.zeros_like(b, shape=A.shape[-1:] + b.shape[1:])
  p = x
  c = 0.

  (x, _, _), _ = lax.scan(f, (x, p, c), length=iters, unroll=unroll)

  return x

