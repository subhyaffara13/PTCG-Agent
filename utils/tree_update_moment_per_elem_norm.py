
def tree_update_moment_per_elem_norm(updates, moments, decay, order):
  """Compute the EMA of the `order`-th moment of the element-wise norm."""

  def orderth_norm(g):
    if jnp.isrealobj(g):
      return g ** order

    half_order = order / 2
    # JAX generates different HLO for int and float `order`
    if half_order.is_integer():
      half_order = int(half_order)
    return numerics.abs_sq(g) ** half_order

  return jax.tree.map(
      lambda g, t: (
          (1 - decay) * orderth_norm(g) + decay * t if g is not None else None
      ),
      updates,
      moments,
      is_leaf=lambda x: x is None,
  )

