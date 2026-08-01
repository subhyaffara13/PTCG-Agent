
def _replace_abstract_array_sharding_with_mesh(
    sds: jax.ShapeDtypeStruct, mesh: jax.sharding.Mesh
) -> jax.ShapeDtypeStruct:
  assert isinstance(sds.sharding, jax.sharding.NamedSharding)
  return sds.update(
      sharding=jax.sharding.NamedSharding(mesh, sds.sharding.spec)
  )


def _replace_abstract_array_sharding_with_mesh(
    sds: jax.ShapeDtypeStruct, mesh: jax.sharding.Mesh
) -> jax.ShapeDtypeStruct:
  assert isinstance(sds.sharding, jax.sharding.NamedSharding)
  sds.sharding = jax.sharding.NamedSharding(mesh, sds.sharding.spec)
  return sds

