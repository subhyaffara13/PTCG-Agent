
def _with_sharding_constraint(
  x: Array,
  axis_resources: jax.sharding.PartitionSpec | None,
  mesh: jax.sharding.Mesh | None = None,
):
  """Wrapper for lax.with_sharding_constraint, no-op on cpu or outside jit."""
  if not meta.global_mesh_defined() and mesh is None:
    return x
  else:
    if mesh is not None and axis_resources is not None:
      sharding = jax.sharding.NamedSharding(mesh, axis_resources)
      return lax.with_sharding_constraint(x, sharding)
    return lax.with_sharding_constraint(x, axis_resources)

