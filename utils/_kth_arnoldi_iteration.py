
def _kth_arnoldi_iteration(k, A, M, V, H):
  """
  Performs a single (the k'th) step of the Arnoldi process. Thus,
  adds a new orthonormalized Krylov vector A(M(V[:, k])) to V[:, k+1],
  and that vectors overlaps with the existing Krylov vectors to
  H[k, :]. The tolerance 'tol' sets the threshold at which an invariant
  subspace is declared to have been found, in which case in which case the new
  vector is taken to be the zero vector.
  """
  dtype, _ = dtypes.lattice_result_type(*tree_leaves(V))
  eps = dtypes.finfo(dtype).eps

  v = tree_map(lambda x: x[..., k], V)  # Gets V[:, k]
  v = M(A(v))
  _, v_norm_0 = _safe_normalize(v)
  v, h = _iterative_classical_gram_schmidt(V, v, v_norm_0, max_iterations=2)

  tol = eps * v_norm_0
  unit_v, v_norm_1 = _safe_normalize(v, thresh=tol)
  V = tree_map(lambda X, y: X.at[..., k + 1].set(y), V, unit_v)

  h = h.at[k + 1].set(v_norm_1.astype(dtype))
  H = H.at[k, :].set(h)
  breakdown = v_norm_1 == 0.
  return V, H, breakdown

