
def _unreduce_named_sharding(reduced_mesh, spec, memory_kind):
  mesh = reduced_mesh[0](*reduced_mesh[1])
  return jax.NamedSharding(mesh, spec, memory_kind=memory_kind)

