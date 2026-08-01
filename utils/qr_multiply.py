
def qr_multiply(a, c, mode='right', pivoting=False, conjugate=False,
                overwrite_a=False, overwrite_c=False):
    """
    Calculate the QR decomposition and multiply Q with a matrix.

    Calculate the decomposition ``A = Q R`` where Q is unitary/orthogonal
    and R upper triangular. Multiply Q with a vector or a matrix c.

    Parameters
    ----------
    a : (M, N), array_like
        Input array
    c : array_like
        Input array to be multiplied by ``q``.
    mode : {'left', 'right'}, optional
        ``Q @ c`` is returned if mode is 'left', ``c @ Q`` is returned if
        mode is 'right'.
        The shape of c must be appropriate for the matrix multiplications,
        if mode is 'left', ``min(a.shape) == c.shape[0]``,
        if mode is 'right', ``a.shape[0] == c.shape[1]``.
    pivoting : bool, optional
        Whether or not factorization should include pivoting for rank-revealing
        qr decomposition, see the documentation of qr.
    conjugate : bool, optional
        Whether Q should be complex-conjugated. This might be faster
        than explicit conjugation.
    overwrite_a : bool, optional
        Whether to overwrite data in `a` (may improve performance). Default is False.
        See :ref:`tutorial_linalg_overwrite` for details.
    overwrite_c : bool, optional
        Whether data in c is overwritten (may improve performance).
        If this is used, c must be big enough to keep the result,
        i.e. ``c.shape[0]`` = ``a.shape[0]`` if mode is 'left'.
        See :ref:`tutorial_linalg_overwrite` for details.

    Returns
    -------
    CQ : ndarray
        The product of ``Q`` and ``c``.
    R : (K, N), ndarray
        R array of the resulting QR factorization where ``K = min(M, N)``.
    P : (N,) ndarray
        Integer pivot array. Only returned when ``pivoting=True``.

    Raises
    ------
    LinAlgError
        Raised if QR decomposition fails.

    Notes
    -----
    This is an interface to the LAPACK routines ``?GEQRF``, ``?ORMQR``,
    ``?UNMQR``, and ``?GEQP3``.

    .. versionadded:: 0.11.0

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.linalg import qr_multiply, qr
    >>> A = np.array([[1, 3, 3], [2, 3, 2], [2, 3, 3], [1, 3, 2]])
    >>> qc, r1, piv1 = qr_multiply(A, 2*np.eye(4), pivoting=1)
    >>> qc
    array([[-1.,  1., -1.],
           [-1., -1.,  1.],
           [-1., -1., -1.],
           [-1.,  1.,  1.]])
    >>> r1
    array([[-6., -3., -5.            ],
           [ 0., -1., -1.11022302e-16],
           [ 0.,  0., -1.            ]])
    >>> piv1
    array([1, 0, 2], dtype=int32)
    >>> q2, r2, piv2 = qr(A, mode='economic', pivoting=1)
    >>> np.allclose(2*q2 - qc, np.zeros((4, 3)))
    True

    """
    if mode not in ['left', 'right']:
        raise ValueError("Mode argument can only be 'left' or 'right' but "
                         f"not '{mode}'")
    c = np.asarray_chkfinite(c)
    if c.ndim < 2:
        onedim = True
        c = np.atleast_2d(c)
        if mode == "left":
            c = c.T
    else:
        onedim = False

    a = np.atleast_2d(np.asarray(a))  # chkfinite done in qr
    M, N = a.shape

    if mode == 'left':
        if c.shape[0] != min(M, N + overwrite_c*(M-N)):
            raise ValueError('Array shapes are not compatible for Q @ c'
                             f' operation: {a.shape} vs {c.shape}')
    else:
        if M != c.shape[1]:
            raise ValueError('Array shapes are not compatible for c @ Q'
                             f' operation: {c.shape} vs {a.shape}')

    raw = qr(a, overwrite_a, mode="raw", pivoting=pivoting)
    Q, tau = raw[0]

    # accommodate empty arrays
    if c.size == 0:
        return (np.empty_like(c),) + raw[1:]

    gor_un_mqr, = get_lapack_funcs(('ormqr',), (Q,))
    if gor_un_mqr.typecode in ('s', 'd'):
        trans = "T"
    else:
        trans = "C"

    Q = Q[:, :min(M, N)]
    if M > N and mode == "left" and not overwrite_c:
        if conjugate:
            cc = np.zeros((c.shape[1], M), dtype=c.dtype, order="F")
            cc[:, :N] = c.T
        else:
            cc = np.zeros((M, c.shape[1]), dtype=c.dtype, order="F")
            cc[:N, :] = c
            trans = "N"
        if conjugate:
            lr = "R"
        else:
            lr = "L"
        overwrite_c = True
    elif c.flags["C_CONTIGUOUS"] and trans == "T" or conjugate:
        cc = c.T
        if mode == "left":
            lr = "R"
        else:
            lr = "L"
    else:
        trans = "N"
        cc = c
        if mode == "left":
            lr = "L"
        else:
            lr = "R"
    cQ, = safecall(gor_un_mqr, "gormqr/gunmqr", lr, trans, Q, tau, cc,
                   overwrite_c=overwrite_c)
    if trans != "N":
        cQ = cQ.T
    if mode == "right":
        cQ = cQ[:, :min(M, N)]
    if onedim:
        cQ = cQ.ravel()

    return (cQ,) + raw[1:]


def qr_multiply(a: ArrayLike, c: ArrayLike, mode: str = 'right',
                pivoting: Literal[False] = False, conjugate: bool = False,
                overwrite_a: bool = False, overwrite_c: bool = False
                ) -> tuple[Array, Array]: ...


def qr_multiply(a: ArrayLike, c: ArrayLike, mode: str = 'right',
                pivoting: Literal[True] = True, conjugate: bool = False,
                overwrite_a: bool = False, overwrite_c: bool = False
                ) -> tuple[Array, Array, Array]: ...


def qr_multiply(a: ArrayLike, c: ArrayLike, mode: str = 'right',
                pivoting: bool = False, conjugate: bool = False,
                overwrite_a: bool = False, overwrite_c: bool = False
                ) -> tuple[Array, Array] | tuple[Array, Array, Array]: ...


def qr_multiply(a: ArrayLike, c: ArrayLike, mode: str = 'right',
                pivoting: bool = False, conjugate: bool = False,
                overwrite_a: bool = False, overwrite_c: bool = False
                ) -> tuple[Array, Array] | tuple[Array, Array, Array]:
  """Calculate the QR decomposition and multiply Q with a matrix.

  JAX implementation of :func:`scipy.linalg.qr_multiply`.

  Args:
    a: array of shape ``(..., M, N)``. Matrix to be decomposed.
    c: array to be multiplied by Q. For ``mode='left'``, ``c`` has shape
      ``(..., K, P)`` where ``K = min(M, N)``. For ``mode='right'``, ``c``
      has shape ``(..., P, M)``. 1-D arrays are supported: for
      ``mode='left'``, treated as a length-``K`` column vector; for
      ``mode='right'``, treated as a length-``M`` row vector. The result
      is raveled back to 1-D in either case.
    mode: ``'right'`` (default) or ``'left'``.

      - ``'left'``: compute ``Q @ c`` (or ``conj(Q) @ c`` if ``conjugate=True``)
        and return ``(Q @ c, R)`` with result shape ``(..., M, P)``
      - ``'right'``: compute ``c @ Q`` (or ``c @ conj(Q)`` if ``conjugate=True``)
        and return ``(c @ Q, R)`` with result shape ``(..., P, K)`` where
        ``K = min(M, N)``
    pivoting: Allows the QR decomposition to be rank-revealing. If ``True``, compute
      the column-pivoted QR decomposition and return permutation indices
      as a third element.
    conjugate: If ``True``, use ``conj(Q)`` (element-wise complex conjugate)
      instead of ``Q``. For real arrays this has no effect.
    overwrite_a: unused in JAX
    overwrite_c: unused in JAX

  Returns:
    If ``pivoting`` is ``False``: ``(result, R)``

    If ``pivoting`` is ``True``: ``(result, R, P)``

  See also:
    - :func:`jax.scipy.linalg.qr`: SciPy-style QR decomposition API
    - :func:`jax.lax.linalg.ormqr`: XLA-style Q-multiply primitive

  Examples:
    Use :func:`qr_multiply` to efficiently solve a least-squares problem.
    For an overdetermined system ``A @ x ≈ b``, pass ``b`` as a 1-D row
    via ``mode='right'`` to obtain ``Q^T @ b`` and ``R`` in one step:

    >>> import jax
    >>> import jax.numpy as jnp
    >>> A = jnp.array([[1., 1.], [1., 2.], [1., 3.], [1., 4.]])
    >>> b = jnp.array([2., 4., 5., 4.])
    >>> Qtb, R = jax.scipy.linalg.qr_multiply(A, b, mode='right')
    >>> x = jax.scipy.linalg.solve_triangular(R, Qtb)
    >>> jnp.allclose(A.T @ A @ x, A.T @ b)
    Array(True, dtype=bool)
  """
  del overwrite_a, overwrite_c  # unused
  a, c = promote_dtypes_inexact(jnp.asarray(a), jnp.asarray(c))
  if mode not in ('right', 'left'):
    raise ValueError(f"mode must be 'right' or 'left', got {mode!r}")

  onedim = c.ndim == 1
  if onedim:
    c = c[:, None] if mode == 'left' else c[None, :]

  m, n = a.shape[-2:]
  k = min(m, n)

  if mode == 'left':
    if c.shape[-2] != k:
      raise ValueError(
          f"Array shapes are not compatible for Q @ c operation: "
          f"a has shape {tuple(a.shape)} so Q has {k} columns, "
          f"but c has {c.shape[-2]} rows (expected {k}).")
  else:
    if c.shape[-1] != m:
      raise ValueError(
          f"Array shapes are not compatible for c @ Q operation: "
          f"a has shape {tuple(a.shape)} so Q has {m} rows, "
          f"but c has {c.shape[-1]} columns (expected {m}).")

  batch = jnp.broadcast_shapes(a.shape[:-2], c.shape[:-2])
  a = jnp.broadcast_to(a, batch + a.shape[-2:])
  c = jnp.broadcast_to(c, batch + c.shape[-2:])

  p: Array | None = None
  if pivoting:
    jpvt = jnp.zeros(a.shape[:-2] + (n,), dtype=jnp.int32)
    r, p, taus = lax_linalg.geqp3(a, jpvt)
    p -= 1  # Convert geqp3's 1-based indices to 0-based indices by subtracting 1.
  else:
    r, taus = lax_linalg.geqrf(a)

  if m > n and mode == 'left':
    zeros = jnp.zeros(c.shape[:-2] + (m - k,) + c.shape[-1:], dtype=c.dtype)
    c = jnp.concatenate([c, zeros], axis=-2)

  if conjugate:
    # Avoid explicit jnp.conj call by instead transposing (for free under jit)
    # and telling LAPACK to compute Hermitian
    c = c.swapaxes(-1, -2)

  # conjugate swaps left/right because c and Q change sides when transposing.
  left = (mode == 'left') != conjugate
  cQ = lax_linalg.ormqr(r, taus, c, left=left, transpose=conjugate)

  if conjugate:
    cQ = cQ.swapaxes(-1, -2)

  if mode == 'right':
    cQ = cQ[..., :k]

  if onedim:
    cQ = cQ.ravel()

  r = jnp.triu(r[..., :k, :])

  if pivoting:
    assert p is not None
    return cQ, r, p
  return cQ, r

