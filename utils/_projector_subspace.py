
def _projector_subspace(P, H, n, rank, maxiter=2, swap=False):
  """Decomposes the `n x n` rank `rank` Hermitian projector `P` into

  an `n x rank` isometry `V_minus` such that `P = V_minus @ V_minus.conj().T`
  and an `n x (n - rank)` isometry `V_minus` such that
  -(I - P) = V_plus @ V_plus.conj().T`.

  The subspaces are computed using the naiive QR eigendecomposition
  algorithm, which converges very quickly due to the sharp separation
  between the relevant eigenvalues of the projector.

  Args:
    P: A rank-`rank` Hermitian projector into the space of `H`'s first `rank`
      eigenpairs. `P` is padded to NxN.
    H: The aforementioned Hermitian matrix, which is used to track convergence.
    n: the true (dynamic) shape of `P`.
    rank: Rank of `P`.
    maxiter: Maximum number of iterations.
    swap: If true, the two outputs spaces are swapped.

  Returns:
    V_minus, V_plus: Isometries into the eigenspaces described in the docstring.
  """
  # Choose an initial guess: the `rank` largest-norm columns of P.
  N, _ = P.shape
  negative_column_norms = -jnp_linalg.norm(P, axis=1)
  # `jnp.argsort` ensures NaNs sort last, so set masked-out column norms to NaN.
  negative_column_norms = _mask(negative_column_norms, (n,), np.nan)
  sort_idxs = jnp.argsort(negative_column_norms)
  X = P[:, sort_idxs]
  # X = X[:, :rank]
  X = _mask(X, (n, rank))

  H_norm = jnp_linalg.norm(H)
  thresh = 10.0 * float(dtypes.finfo(X.dtype).eps) * H_norm

  # First iteration skips the matmul.
  def body_f_after_matmul(X):
    Q, _ = jnp_linalg.qr(X, mode="complete")
    # V1 = Q[:, :rank]
    # V2 = Q[:, rank:]
    V1 = _mask(Q, (n, rank))
    V2 = _slice(Q, (0, rank), (n, n - rank), (N, N))

    # TODO: might be able to get away with lower precision here
    error_matrix = tensor_contractions.dot(V2.conj().T, H)
    error_matrix = tensor_contractions.dot(error_matrix, V1)
    error = jnp_linalg.norm(error_matrix)
    return V1, V2, error

  def cond_f(args):
    _, _, j, error = args
    still_counting = j < maxiter
    unconverged = error > thresh
    return ufuncs.logical_and(still_counting, unconverged)[0]

  def body_f(args):
    V1, _, j, _ = args
    X = tensor_contractions.dot(P, V1)
    V1, V2, error = body_f_after_matmul(X)
    return V1, V2, j + 1, error

  V1, V2, error = body_f_after_matmul(X)
  one = jnp.ones(1, dtype=np.int32)
  V1, V2, _, error = lax.while_loop(cond_f, body_f, (V1, V2, one, error))
  if swap:
    return V2, V1
  else:
    return V1, V2

