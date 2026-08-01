
def split_spectrum(H, n, split_point, V0=None):
  """ The Hermitian matrix `H` is split into two matrices `H_minus`
  `H_plus`, respectively sharing its eigenspaces beneath and above
  its `split_point`th eigenvalue.

  Returns, in addition, `V_minus` and `V_plus`, isometries such that
  `Hi = Vi.conj().T @ H @ Vi`. If `V0` is not None, `V0 @ Vi` are
  returned instead; this allows the overall isometries mapping from
  an initial input matrix to progressively smaller blocks to be formed.

  Args:
    H: The Hermitian matrix to split.
    split_point: The eigenvalue to split along.
    V0: Matrix of isometries to be updated.
  Returns:
    H_minus: A Hermitian matrix sharing the eigenvalues of `H` beneath
      `split_point`.
    V_minus: An isometry from the input space of `V0` to `H_minus`.
    H_plus: A Hermitian matrix sharing the eigenvalues of `H` above
      `split_point`.
    V_plus: An isometry from the input space of `V0` to `H_plus`.
    rank: The dynamic size of the m subblock.
  """
  N, _ = H.shape
  H_shift = H - (split_point * jnp.eye(N, dtype=split_point.dtype)).astype(H.dtype)
  U, _, _, _ = qdwh.qdwh(H_shift, is_hermitian=True, dynamic_shape=(n, n))
  I = _mask(jnp.eye(N, dtype=H.dtype), (n, n))
  P_minus = -0.5 * (U - I)
  rank_minus = jnp.round(jnp.trace(ufuncs.real(P_minus))).astype(np.int32)
  P_plus = 0.5 * (U + I)
  rank_plus = n - rank_minus

  # Run subspace iteration on whichever projector P_minus or P_plus that has the
  # smallest rank. This can save a significant amount of work when H has
  # rank << n or if our estimate of the median eigenvalue is poor, because
  # the subspace iteration involves computing the QR decomposition of a
  # matrix of size n x rank.
  swap = rank_plus < rank_minus
  V_minus, V_plus = lax.cond(
      swap,
      lambda: _projector_subspace(P_plus, H, n, rank_plus, swap=True),
      lambda: _projector_subspace(P_minus, H, n, rank_minus, swap=False),
  )
  H_minus = (V_minus.conj().T @ H) @ V_minus
  H_plus = (V_plus.conj().T @ H) @ V_plus
  if V0 is not None:
    V_minus = tensor_contractions.dot(V0, V_minus)
    V_plus = tensor_contractions.dot(V0, V_plus)
  return H_minus, V_minus, H_plus, V_plus, rank_minus

