
def _generate_diagnostics(prev_XPR, X, P, R, theta, converged, adj_resid):
  k = X.shape[1]
  assert X.shape == P.shape

  diagdiag = lambda x: jnp.diag(jnp.diag(x))
  abserr = lambda x: jnp.abs(x).sum() / (k ** 2)

  XTX = _mm(X.T, X)
  DX = diagdiag(XTX)
  orthX = abserr(XTX - DX)

  PTP = _mm(P.T, P)
  DP = diagdiag(PTP)
  orthP = abserr(PTP - DP)

  PX = abserr(X.T @ P)

  prev_basis = prev_XPR.shape[1] - jnp.sum(jnp.all(prev_XPR == 0.0, axis=0))

  return {
      'basis rank': prev_basis,
      'X zeros': jnp.sum(jnp.all(X == 0.0, axis=0)),
      'P zeros': jnp.sum(jnp.all(P == 0.0, axis=0)),
      'lambda history': theta[:k],
      'residual history': jnp.linalg.norm(R, axis=0, ord=2),
      'converged': converged,
      'adjusted residual max': jnp.max(adj_resid),
      'adjusted residual p50': jnp.median(adj_resid),
      'adjusted residual min': jnp.min(adj_resid),
      'X orth': orthX,
      'P orth': orthP,
      'P.X': PX}

