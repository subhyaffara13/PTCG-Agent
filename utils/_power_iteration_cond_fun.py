
def _power_iteration_cond_fun(error_tolerance, num_iters, loop_vars):
  normalized_eigvec, unnormalized_eigvec, eig, iter_num = loop_vars
  residual = optax.tree.sub(
      unnormalized_eigvec, optax.tree.scale(eig, normalized_eigvec)
  )
  residual_norm = optax.tree.norm(residual)
  converged = jnp.abs(residual_norm / eig) < error_tolerance
  return ~converged & (iter_num < num_iters)

