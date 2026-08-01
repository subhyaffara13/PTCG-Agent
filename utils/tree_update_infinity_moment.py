
def tree_update_infinity_moment(updates, moments, decay, eps):
  """Compute the exponential moving average of the infinity norm."""
  return jax.tree.map(
      lambda g, t: (
          jnp.maximum(jnp.abs(g) + eps, decay * t) if g is not None else g
      ),
      updates,
      moments,
      is_leaf=lambda x: x is None,
  )

