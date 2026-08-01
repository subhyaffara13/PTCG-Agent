
def _gmres_batched(A, b, x0, unit_residual, residual_norm, ptol, restart, M):
  """
  Implements a single restart of GMRES. The ``restart``-dimensional Krylov
  subspace
  K(A, x0) = span(A(x0), A@x0, A@A@x0, ..., A^restart @ x0) is built, and the
  projection of the true solution into this subspace is returned.

  This implementation solves a dense linear problem instead of building
  a QR factorization during the Arnoldi process.
  """
  del ptol  # unused
  # https://www-users.cs.umn.edu/~saad/Calais/PREC.pdf
  V = tree_map(
      lambda x: jnp.pad(x[..., None], ((0, 0),) * x.ndim + ((0, restart),)),
      unit_residual,
  )
  dtype, weak_type = dtypes.lattice_result_type(*tree_leaves(b))
  H = lax_internal._convert_element_type(
      jnp.eye(restart, restart + 1, dtype=dtype), weak_type=weak_type)

  def loop_cond(carry):
    _, _, breakdown, k = carry
    return jnp.logical_and(k < restart, jnp.logical_not(breakdown))

  def arnoldi_process(carry):
    V, H, _, k = carry
    V, H, breakdown = _kth_arnoldi_iteration(k, A, M, V, H)
    return V, H, breakdown, k + 1

  carry = (V, H, False, 0)
  V, H, _, _ = lax.while_loop(loop_cond, arnoldi_process, carry)

  beta_vec = jnp.zeros_like(H, shape=(restart + 1,)).at[0].set(residual_norm.astype(dtype))
  y = _lstsq(H.T, beta_vec)
  dx = tree_map(lambda X: _dot(X[..., :-1], y), V)

  x = _add(x0, dx)

  residual = M(_sub(b, A(x)))
  unit_residual, residual_norm = _safe_normalize(residual)
  return x, unit_residual, residual_norm

