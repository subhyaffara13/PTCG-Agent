
def _colocated_cpu_mesh_cached(mesh: jax.sharding.Mesh) -> jax.sharding.Mesh:
  """Returns a CPU mesh that is similar to the given mesh but has colocated CPU devices."""
  # Finding colocated CPU devices reuses the cache of `colocated_cpu_devices`
  # called with devices. `_colocated_cpu_mesh` itself is also cached to avoid
  # creating a new `Mesh` object repeatedly.
  flat_cpu_devices = colocated_cpu_devices(tuple(mesh.devices.flat))
  return jax.sharding.Mesh(
      np.array(flat_cpu_devices).reshape(mesh.axis_sizes),
      mesh.axis_names,
      axis_types=mesh.axis_types,
  )

