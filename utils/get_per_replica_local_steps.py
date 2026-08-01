
def get_per_replica_local_steps(
    local_directory: epath.Path,
    *,
    step_name_format: step_lib.NameFormat[step_lib.Metadata],
    global_mesh: jax.sharding.Mesh,
    replica_axis_index: int,
) -> dict[int, set[int]]:
  """Gets the set of steps present in each replica from all hosts."""
  local_steps = set(m.step for m in step_name_format.find_all(local_directory))
  logging.info(
      'Found steps: %s in local host storage: %s.',
      local_steps,
      local_directory,
  )

  all_processes_data = sync_global_data(
      {
          'process_id': multihost.process_index(),
          'steps': list(local_steps),
      },
  )
  per_process_steps = {}
  for data in all_processes_data:
    per_process_steps[data['process_id']] = set(data['steps'])
  per_slice_steps = _common_values_per_replica(
      per_process_steps,
      global_mesh=global_mesh,
      replica_axis_index=replica_axis_index,
  )
  logging.vlog(1, 'per_replica_steps=%s', per_slice_steps)
  return per_slice_steps

