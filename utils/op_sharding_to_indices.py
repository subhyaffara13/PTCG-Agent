
def op_sharding_to_indices(
    op_sharding: xc.HloSharding, shape: Sequence[int],
    num_devices: int) -> tuple[tuple[slice, ...], ...]:
  indices = op_sharding_to_numpy_indices(op_sharding, shape, num_devices)
  return tuple(indices.flat)

