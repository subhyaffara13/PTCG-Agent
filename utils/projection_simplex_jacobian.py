
def projection_simplex_jacobian(projection):
  """Theoretical expression for the Jacobian of projection_simplex."""
  support = (projection > 0).astype(jnp.int32)
  cardinality = jnp.count_nonzero(support)
  return jnp.diag(support) - jnp.outer(support, support) / cardinality

