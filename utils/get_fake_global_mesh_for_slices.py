from typing import List, Set

def get_fake_global_mesh_for_slices(
    slice_processes: List[Set[int]],
    replica_axis_index: int = 0,
) -> jax.sharding.Mesh:
  """Creates a "multi-slice" global mesh for testing.

  Args:
    slice_processes: List of sets of process indices, where each element in the
      list is a set of processes that are active in a single slice.
    replica_axis_index: The index of the replica axis in the global mesh.

  Returns:
    A global mesh.
  """
  assert replica_axis_index in [0, 1]
  devices = jax.devices()
  slice_devices = []
  devices_per_slices = None
  all_processes = set()
  for processes in slice_processes:
    all_processes |= processes
    slice_devices.append([
        d
        for d in devices
        if multihost.runtime_to_distributed_process_id(d.process_index)
        in processes
    ])
    devices_per_slices = devices_per_slices or len(slice_devices[-1])
    if len(slice_devices[-1]) != devices_per_slices:
      raise ValueError('All slices must have the same number of devices.')
  if len(all_processes) != jax.process_count():
    raise ValueError('All processes must be accounted for.')

  slice_devices = np.asarray(slice_devices)
  axis_names = ('replica', 'data')
  if replica_axis_index == 1:
    slice_devices = np.transpose(slice_devices, (1, 0))
    axis_names = ('data', 'replica')
  return jax.sharding.Mesh(slice_devices, axis_names)

