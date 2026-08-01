
def get_global_mesh() -> jax.sharding.AbstractMesh | jax.sharding.Mesh | None:
  mesh = jax.sharding.get_abstract_mesh()
  if mesh.empty:
    return None
  return mesh

