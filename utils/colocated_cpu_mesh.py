
def colocated_cpu_mesh(mesh: jax.sharding.Mesh) -> jax.sharding.Mesh:
  """Returns a colocated CPU mesh preserving the input mesh order."""
  return cp.colocated_cpu_devices(mesh)

