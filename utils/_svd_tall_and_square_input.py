from typing import Any

def _svd_tall_and_square_input(
    a: Any,
    hermitian: bool,
    compute_uv: bool,
    max_iterations: int,
    subset_by_index: tuple[int, int] | None = None,
) -> Any | Sequence[Any]:
  """Singular value decomposition for m x n matrix and m >= n.

  Args:
    a: A matrix of shape `m x n` with `m >= n`.
    hermitian: True if `a` is Hermitian.
    compute_uv: Whether to also compute `u` and `v` in addition to `s`.
    max_iterations: The predefined maximum number of iterations of QDWH.

  Returns:
    A 3-tuple (`u`, `s`, `v`), where `u` is a unitary matrix of shape `m x n`,
    `s` is vector of length `n` containing the singular values in the descending
    order, `v` is a unitary matrix of shape `n x n`, and
    `a = (u * s) @ v.T.conj()`. For `compute_uv=False`, only `s` is returned.
  """

  u_p, h, _, _ = tpu_qdwh.qdwh(
      a, is_hermitian=hermitian, max_iterations=max_iterations
  )

  # TODO: Uses `eigvals_only=True` if `compute_uv=False`.
  v, s = lax_linalg.eigh(
      h, subset_by_index=subset_by_index, sort_eigenvalues=False
  )

  # Singular values are non-negative by definition. But eigh could return small
  # negative values, so we clamp them to zero.
  s = jnp.maximum(s, 0.0)

  # Sort or reorder singular values to be in descending order.
  sort_idx = jnp.argsort(s, descending=True)
  s_out = s[sort_idx]

  if not compute_uv:
    return s_out

  # Reorders eigenvectors.
  v_out = v[:, sort_idx]
  u_out = u_p @ v_out

  # Makes correction if computed `u` from qdwh is not unitary.
  # Section 5.5 of Nakatsukasa, Yuji, and Nicholas J. Higham. "Stable and
  # efficient spectral divide and conquer algorithms for the symmetric
  # eigenvalue decomposition and the SVD." SIAM Journal on Scientific Computing
  # 35, no. 3 (2013): A1325-A1349.
  def correct_rank_deficiency(u_out):
    u_out, r = lax_linalg.qr(u_out, full_matrices=False)
    u_out = u_out @ jnp.diag(jnp.where(jnp.diag(r) >= 0, 1, -1))
    return u_out

  eps = float(dtypes.finfo(a.dtype).eps)
  do_correction = s_out[-1] <= a.shape[1] * eps * s_out[0]
  cond_f = lambda args: args[1]
  body_f = lambda args: (correct_rank_deficiency(args[0]), False)
  u_out, _ = lax.while_loop(cond_f, body_f, (u_out, do_correction))
  return (u_out, s_out, v_out)

