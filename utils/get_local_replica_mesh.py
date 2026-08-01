
def get_local_replica_mesh(
    mesh: jax.sharding.Mesh, replica_axis_index: int
) -> jax.sharding.Mesh:
  """Returns the local replica mesh for the given global mesh."""
  return jax.sharding.Mesh(
      np.expand_dims(
          multislice.local_replica_devices(
              mesh, replica_axis_index=replica_axis_index
          ),
          axis=replica_axis_index,
      ),
      mesh.axis_names,
  )

