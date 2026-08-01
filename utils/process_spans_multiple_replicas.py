
def process_spans_multiple_replicas(
    global_mesh: jax.sharding.Mesh,
    *,
    replica_axis_index: int = 0,
) -> bool:
  """Checks if any JAX process controls devices across different replicas.

  Replicas are defined by slicing the `global_mesh` along the
  `replica_axis_index`. This function iterates through all unique JAX processes
  and, for each process, checks if the devices it manages belong to more than
  one replica group.

  Args:
    global_mesh: The global JAX mesh.
    replica_axis_index: The index of the axis in the mesh shape that
      differentiates the replicas.

  Returns:
    True if at least one process has devices in multiple replicas,
    False otherwise.
  """
  num_replicas = replica_count(
      global_mesh, replica_axis_index=replica_axis_index
  )
  all_processes = multihost.unique_processes_from_devices(
      global_mesh.devices.flatten()
  )

  for process_idx in all_processes:
    found_replica_ids = []
    for replica_id in range(num_replicas):
      devices_in_replica = replica_devices(
          global_mesh,
          replica_id=replica_id,
          replica_axis_index=replica_axis_index,
      )
      if process_idx in multihost.unique_processes_from_devices(
          devices_in_replica
      ):
        found_replica_ids.append(replica_id)

    if len(found_replica_ids) > 1:
      return True
  return False

