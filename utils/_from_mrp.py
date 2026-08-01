
def _from_mrp(mrp: Array) -> Array:
  mrp_squared_plus_1 = jnp.dot(mrp, mrp) + 1
  return jnp.hstack([2 * mrp[:3], (2 - mrp_squared_plus_1)]) / mrp_squared_plus_1

