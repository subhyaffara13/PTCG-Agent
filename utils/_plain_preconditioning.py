
def _plain_preconditioning(
    diff_params_memory: Union[list[jnp.ndarray], jnp.ndarray],
    diff_updates_memory: Union[list[jnp.ndarray], jnp.ndarray],
    updates: jnp.ndarray,
    identity_scale: float = 1.0,
) -> jnp.ndarray:
  """Plain implementation of lbfgs preconditioning."""
  # Algorithm 7.4 in "Numerical Optimization" by Nocedal and Wright, 1999
  # Notations differ from reference above with the following correspondences
  # dws -> s, dus -> y, rhos -> rhos, precond_factor -> V, precond_mat -> H,
  # identity_scale -> gamma

  # 1. Operates on list of vectors rather than stacked trees.
  # 2. Computes weights (rhos) of the rank one matrices directly rather than
  # accessing these weights from past memory.
  # 3. Uses plain for loops rather than scan.

  # Shorten names for better readability in terms of math, see
  # :func:`optax.scale_by_lbfgs` for mathematical formulas.
  dws, dus = diff_params_memory, diff_updates_memory
  # m below is the memory size
  m = len(dws)

  if m == 0:
    return identity_scale * updates

  dws = jnp.array(dws)
  dus = jnp.array(dus)

  rhos = jnp.zeros(m)
  alphas = jnp.zeros(m)

  # Compute right product.
  def right_product(j, tup):
    rhos, alphas, u = tup
    i = m - j - 1
    # rhos[i] = 1. / jnp.sum(dws[i] * dus[i])
    rhos = rhos.at[i].set(1.0 / jnp.sum(dws[i] * dus[i]))
    # alphas[i] = rhos[i] * jnp.sum(dws[i] * r)
    alphas = alphas.at[i].set(rhos[i] * jnp.sum(dws[i] * u))
    u = u - alphas[i] * dus[i]
    return rhos, alphas, u

  # for i in reversed(range(m)):
  rhos, alphas, pu = jax.lax.fori_loop(
      0, m, right_product, (rhos, alphas, updates)
  )

  pu = pu * identity_scale

  # Compute left product.
  def left_product(i, u):
    beta = rhos[i] * jnp.sum(dus[i] * u)
    return u + dws[i] * (alphas[i] - beta)

  # for i in range(m):
  pu = jax.lax.fori_loop(0, m, left_product, pu)

  return pu

