
def _solve_sylvester_2d(A: Array, B: Array, C: Array, *, method: str, tol: float) -> Array:
  m, n = C.shape[-2:]
  if method == "schur":
    R, U = schur(A, output='complex')
    S, V = schur(B.conj().T, output='complex')
    F = U.conj().T @ C.astype(R.dtype) @ V
    Y = _solve_sylvester_triangular_scan(R, S.conj().T, F)
    X = U @ Y @ V.conj().T
  elif method == "eigen":
    RA, UA = jnp.linalg.eig(A)
    RB, UB = jnp.linalg.eig(B)
    F = solve(UA, C.astype(RA.dtype) @ UB)
    W = RA[:, None] + RB[None, :]
    Y = F / W
    X = UA[:m,:m] @ Y[:m,:n] @ inv(UB)[:n,:n]
  else:
    raise ValueError(f"Unrecognized method {method}. The two valid methods are either \"schur\" or \"eigen\".")
  if not dtypes.issubdtype(C.dtype, np.complexfloating):
    X = X.real
  return lax.cond(
    jnp.any(jnp.abs(jnp.linalg.eigvals(A)[:, None] + jnp.linalg.eigvals(B)[None, :]) < tol),
    lambda: jnp.zeros_like(X) * np.nan,
    lambda: X,
  )

