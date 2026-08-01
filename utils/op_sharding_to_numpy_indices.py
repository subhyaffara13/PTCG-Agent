
def op_sharding_to_numpy_indices(
    hlo_sharding: xc.HloSharding, shape: Sequence[int],
    num_devices: int) -> np.ndarray:
  indices = np.empty(num_devices, dtype=np.object_)

  # num_devices is required as an argument when hlo_sharding is
  # REPLICATED. `jax.device_count()` cannot be used because you can create
  # an opsharding with less number of devices than `jax.device_count()`.
  if is_hlo_sharding_replicated(hlo_sharding):
    indices.fill((slice(None),) * len(shape))
    return indices

  assert num_devices == hlo_sharding.num_devices()

  partitions, num_replicas = get_num_ways_dim_sharded(hlo_sharding)
  assert len(partitions) == len(shape), (len(partitions), len(shape))

  axis_indices: list[Sequence[_Index]] = []
  for dim, n_shards in zip(shape, partitions):
    if n_shards == 1:
      axis_indices.append([slice(None)])
    elif n_shards > 1:
      shard_size, ragged = divmod(dim, n_shards)
      assert not ragged, (dim, n_shards)
      axis_indices.append([slice(i * shard_size, (i + 1) * shard_size)
                           for i in range(n_shards)])
    else:
      raise AssertionError('Unrecognized number of shards. Please file a bug!')

  device_it = iter(hlo_sharding.tile_assignment_devices())

  for idxs in itertools.product(*axis_indices):
    for _ in range(num_replicas):
      indices[next(device_it)] = idxs
  return indices

