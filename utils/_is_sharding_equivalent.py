
def _is_sharding_equivalent(sharding_a, sharding_b, ndim):
  """Check if sharding is equivalent to NamedSharding(mesh.local_mesh, pspec)."""
  return sharding_a.is_equivalent_to(sharding_b, ndim)

