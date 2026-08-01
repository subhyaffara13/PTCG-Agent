
def get_process_index_and_count(
    tensor_sharding: jsharding.Sharding, dim: int, ndims: int) -> tuple[int, int]:
  """Get current process index and number of unique processes for given dimension.

  This function facilitates mapping of process-level data to individual
  devices. Each process can use its index to obtain the data corresponding
  to that index. If process level data is sharded on multiple dimensions
  this function can be used to build the cross product of indices in
  each sharded axis. Processes that need to load the same data will have
  the same index. For shardings whose per-process data is not distributed
  on a grid, the number of distinct shards will be such that it is possible to
  build the target shape while maintaining a "cube" shape of local-process data.

  For example, in case of 4 hosts with sharding distributed like so:

  1234
  2143

  For dim 0 (rows): all processes need to access all rows, so we return (0, 1)
  For dim 1 (cols):
     process 1 and 2 returns index 0 out of 2 (need cols 0 and 1),
     process 3 and 4 returns index 1 out of 2 (need cols 2 and 3).

  On the other hand, for a sharding like:

  1212
  3434

  Dim 0 (rows): process 1 and 2 returns (0, 2), process 3 and 4 returns (1, 2)
  Dim 1 (cols): process 1 and 3 returns (0, 2), process 2 and 4 returns (1, 2)

  Note: This function requires sharding to be process uniform in dimension
  `dim`:
   each process has the same number of addressable indices in that
  dimension and all index sets across processes are either disjoint or the same.

  For sharding to be process uniform the addressable shards doesn't need to
  form contiguous subtensor, or even a sparse grid  and  in case of
  interleaved high-dimensional tensor it is possible for sharding to be
  process uniform only in some dimensions but not others.

  For example:
    1111 and 12 and 1212 and 1212
    2222     21     2121     1212

  are all sharding uniform, in both dimensions. However

    1122
    2121
    1121
    1222

  is uniform in dimension 0 (both hosts access all rows), but
  is not uniform in dimension 1 (host 1 accesses columns: 0, 1, and 3),
  while host 2 accesses (0, 1, 2, 3).

  Returns:
    A tuple of (index, num_distinct_shards) for the given dimension.
    It is guaranteed that `index` will cover 0 to `num_distinct_shards - 1`,
    across all processes.

  Raises:
    NonUniformShardingError: if the sharding is not process uniform in dimension
    `dim`.
  """
  # TODO(sandler, yashkatariya): Consider making this function public.

  if (tensor_sharding.is_fully_addressable or
      tensor_sharding.is_fully_replicated):
    return (0, 1)
  # Get device to indices map, we don't care about the concrete
  # global shape here, only to get the distribution of shards across the tensor
  # using (num_devices, num_devices, ...)  This is a universal shape that is
  # compatible with any mesh with num_devices.
  device_map = tensor_sharding.devices_indices_map(
      (tensor_sharding.num_devices,) * ndims)

  # Get the slices for 'dim' for all devices.
  global_slice = {k: v[dim] for k, v in device_map.items()}

  # Contains mapping from process_index to a set of slices for that process.
  process_to_slice = collections.defaultdict(set)
  # Contains global set of slices across all processes.
  all_slices = set()

  # Compute the set of slices for each process and the global set of slices.
  for d, v in global_slice.items():
    key = (v.start, v.stop)
    process_to_slice[d.process_index].add(key)
    all_slices.add(key)

  # Get the set of slices for the current process which we will use to compute
  # the index of the current process.
  current_pid = next(iter(tensor_sharding.addressable_devices)).process_index
  addressable_slices = frozenset(process_to_slice[current_pid])

  # Verify that all processes have the same number of slices.
  slices_per_process = len(addressable_slices)
  if any(len(x) != slices_per_process for x in process_to_slice.values()):
    raise NonUniformShardingError(
        f'{tensor_sharding=} is non-uniform on {dim=} as some processes have '
        'different number of slices.'
    )
  unique_processes = list({frozenset(x) for x in process_to_slice.values()})

  # After removing duplicate processes all unique slices should
  # cover the dimension exactly once. If they don' it means that
  # the sharding is not uniform.
  if sum(len(h) for h in unique_processes) != len(all_slices):
    raise NonUniformShardingError(
        f'{tensor_sharding=} is non-uniform on {dim=}'
    )
  return (unique_processes.index(addressable_slices), len(unique_processes))

