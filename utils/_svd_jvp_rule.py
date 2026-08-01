
def _svd_jvp_rule(
    primals, tangents, *, full_matrices, compute_uv, subset_by_index,
    algorithm=None,
):
  A, = primals
  dA, = tangents
  s, U, Vt = svd_p.bind(
      A, full_matrices=False, compute_uv=True, subset_by_index=subset_by_index,
      algorithm=algorithm,
  )

  if (
      compute_uv
      and full_matrices
      and not core.definitely_equal(A.shape[-2], A.shape[-1])
  ):
    # TODO: implement full matrices case, documented here: https://people.maths.ox.ac.uk/gilesm/files/NA-08-01.pdf
    raise NotImplementedError(
      "Singular value decomposition JVP not implemented for full matrices")

  Ut, V = _H(U), _H(Vt)
  s_dim = s[..., None, :]
  dS = Ut @ dA @ V
  ds = _extract_diagonal(dS.real)

  if not compute_uv:
    return (s,), (ds,)

  s_diffs = (s_dim + _T(s_dim)) * (s_dim - _T(s_dim))
  s_diffs_zeros = lax._eye(s.dtype, (s.shape[-1], s.shape[-1]))  # jnp.ones((), dtype=A.dtype) * (s_diffs == 0.)  # is 1. where s_diffs is 0. and is 0. everywhere else
  s_diffs_zeros = lax.expand_dims(s_diffs_zeros, range(s_diffs.ndim - 2))
  F = 1 / (s_diffs + s_diffs_zeros) - s_diffs_zeros
  dSS = s_dim.astype(A.dtype) * dS  # dS.dot(jnp.diag(s))
  SdS = _T(s_dim.astype(A.dtype)) * dS  # jnp.diag(s).dot(dS)

  s_zeros = (s == 0).astype(s.dtype)
  s_inv = 1 / (s + s_zeros) - s_zeros
  s_inv_mat = _construct_diagonal(s_inv)
  dUdV_diag = .5 * (dS - _H(dS)) * s_inv_mat.astype(A.dtype)
  dU = U @ (F.astype(A.dtype) * (dSS + _H(dSS)) + dUdV_diag)
  dV = V @ (F.astype(A.dtype) * (SdS + _H(SdS)))

  m, n = A.shape[-2:]
  if m > n:
    dAV = dA @ V
    dU = dU + (dAV - U @ (Ut @ dAV)) / s_dim.astype(A.dtype)
  if n > m:
    dAHU = _H(dA) @ U
    dV = dV + (dAHU - V @ (Vt @ dAHU)) / s_dim.astype(A.dtype)

  return (s, U, Vt), (ds, dU, _H(dV))

