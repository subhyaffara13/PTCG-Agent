
def _reduce_named_sharding(
    sharding: jax.sharding.NamedSharding,
) -> tuple[Callable[..., jax.sharding.NamedSharding], Any]:
  assert isinstance(sharding.mesh, jax.sharding.Mesh), "Only Mesh is supported"
  reduced_mesh = _reduce_mesh(sharding.mesh)
  return _unreduce_named_sharding, (
      reduced_mesh, sharding.spec, sharding.memory_kind)

