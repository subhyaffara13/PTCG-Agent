
def _common_values_per_replica(
    per_process_values: dict[int, set[int]],
    *,
    global_mesh: jax.sharding.Mesh,
    replica_axis_index: int,
) -> dict[int, set[int]]:
  """Obtains values shared in common across all processes in each replica.

  Args:
    per_process_values: A mapping of process index to a list of values local to
      that process.
    global_mesh: The global mesh.
    replica_axis_index: The index of the replica axis in the global mesh.

  Returns:
    A mapping of slice index to a set of values shared in common across all
    processes in that slice. A value appearing in one process but not another
    in the same slice will not appear in the output.
  """
  total_num_replicas = multislice.replica_count(
      global_mesh, replica_axis_index=replica_axis_index
  )
  num_processes_per_replica = (
      global_mesh.devices.size // total_num_replicas // jax.local_device_count()
  )
  per_replica_values = collections.defaultdict(list)
  for pid, values in per_process_values.items():
    replica_id = multislice.process_replica_id(
        pid, global_mesh, replica_axis_index=replica_axis_index
    )
    per_replica_values[replica_id].extend(values)

  for replica_id, values in per_replica_values.items():
    counter = collections.Counter(values)
    common_values = [
        k for k in counter if counter[k] == num_processes_per_replica
    ]
    # Here `len(common_values)`` will be less than or equal to `len(values)`
    # because a value can only appear in `common_values` if it occurs
    # `num_processes_per_slice` times in `values`.
    if len(common_values) > len(values):
      raise AssertionError(
          f' len(common_values) ({common_values}) exceeded length of input'
          f' values ({values}).'
      )
    per_replica_values[replica_id] = common_values

  return {k: set(v) for k, v in per_replica_values.items()}

