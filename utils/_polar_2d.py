
def _polar_2d(a: Array, side: str, method: str, eps: float | None,
              max_iterations: int | None) -> tuple[Array, Array]:
  m, n = a.shape
  if method == "qdwh":
    # TODO(phawkins): return info also if the user opts in?
    if m >= n and side == "right":
      unitary, posdef, _, _ = qdwh.qdwh(a, is_hermitian=False, eps=eps)
    elif m < n and side == "left":
      a = a.T.conj()
      unitary, posdef, _, _ = qdwh.qdwh(a, is_hermitian=False, eps=eps)
      posdef = posdef.T.conj()
      unitary = unitary.T.conj()
    else:
      raise NotImplementedError("method='qdwh' only supports mxn matrices "
                                "where m < n where side='right' and m >= n "
                                f"side='left', got {a.shape} with {side=}")
  elif method == "svd":
    u_svd, s_svd, vh_svd = lax_linalg.svd(a, full_matrices=False)
    s_svd = s_svd.astype(u_svd.dtype)
    unitary = u_svd @ vh_svd
    if side == "right":
      posdef = (vh_svd.T.conj() * s_svd[None, :]) @ vh_svd
    else:
      posdef = (u_svd * s_svd[None, :]) @ (u_svd.T.conj())
  else:
    raise ValueError(f"Unknown polar decomposition method {method}.")
  return unitary, posdef

