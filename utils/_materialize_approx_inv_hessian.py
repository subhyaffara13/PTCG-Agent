
def _materialize_approx_inv_hessian(
    diff_params_memory: jnp.ndarray,
    diff_updates_memory: jnp.ndarray,
    weights_memory: jnp.ndarray,
    memory_idx: int,
) -> jnp.ndarray:
  """Computes approximate inverse hessian in lbfgs as product of matrices."""
  # Equation (7.19) in "Numerical Optimization" by Nocedal and Wright, 1999
  # Notations differ from reference above with the following correspondences
  # dws -> s, dus -> y, rhos -> rhos, V -> V, P -> H

  # Shorten names for better readability in terms of math, see
  # :func:`optax.scale_by_lbfgs` for mathematical formulas.
  dws, dus, rhos = diff_params_memory, diff_updates_memory, weights_memory
  k = memory_idx
  # m below is the memory size
  m, d = diff_params_memory.shape

  dws = jnp.roll(dws, -k, axis=0)
  dus = jnp.roll(dus, -k, axis=0)
  rhos = jnp.roll(rhos, -k, axis=0)

  id_mat = jnp.eye(d, d)
  p = id_mat
  safe_dot = lambda x, y: jnp.dot(x, y, precision=jax.lax.Precision.HIGHEST)

  for j in range(m):
    v = id_mat - rhos[j] * jnp.outer(dus[j], dws[j])
    p = safe_dot(v.T, safe_dot(p, v)) + rhos[j] * jnp.outer(dws[j], dws[j])
  precond_mat = p
  return precond_mat

