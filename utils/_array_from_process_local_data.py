
def _array_from_process_local_data(
    local_data: np.ndarray, sharding: Sharding,
    global_shape: Shape | None = None) -> ArrayImpl:
  # TODO(sandler): consider supporting partially specified global_shape or
  # making local_to_global_shape available in the api.
  local_shape = local_data.shape
  if global_shape is None:
    global_shape = local_to_global_shape(sharding, local_shape)  # pyrefly: ignore[bad-assignment]
    assert global_shape is not None
    if None in global_shape:
      raise ValueError(
          "Unable to compute global_shape due to non-uniform sharding."
          f" Specify global shape directly. Partially computed {global_shape=}."
      )
  elif None in global_shape:
    raise ValueError(f"{global_shape=} has Nones. This is not supported.")
  full_dim = []
  for i, (data_dim, global_dim) in enumerate(
      zip(local_data.shape, global_shape)
  ):
    full_dim.append(data_dim == global_dim)
    if data_dim != global_dim:
      process_slice = num_addressable_indices(sharding, i, global_shape)
      if process_slice != data_dim:
        raise ValueError(
            "Invalid host data, each dimension should match either global or "
            f"process shape. In dimension {i}, the process data has {data_dim} "
            f"elements. Process addresses {process_slice} elements and "
            f"{global_shape=}."
        )
  addressable_shards = sharding.addressable_devices_indices_map(global_shape)
  shard = next(iter(addressable_shards.values()))
  assert shard is not None
  shard_shape = _get_shape_from_index(shard, global_shape)
  slices_for_each_dim: list[list[int]] = [[] for _ in global_shape]
  for shard_index in addressable_shards.values():
    assert shard_index is not None
    for i, slc in enumerate(shard_index):
      slices_for_each_dim[i].append(slc.start or 0)
  for i in range(len(global_shape)):
    slices_for_each_dim[i] = sorted(set(slices_for_each_dim[i]))

  @functools.lru_cache(maxsize=4096)
  def local_slice(i, start):
    # Looks up the index of this slice in the list of slices for this dimension.
    # This will determine the slice in host_local_data
    start = slices_for_each_dim[i].index(start or 0) * shard_shape[i]
    end = start + shard_shape[i]
    return slice(start, end)

  def cb(index: Index | None) -> ArrayLike:
    assert index is not None
    data_slice = (
        slc if full_dim[i] else local_slice(i, slc.start)
        for i, slc in enumerate(index)
    )
    return local_data[tuple(data_slice)]

  return make_array_from_callback(global_shape, sharding, cb)

