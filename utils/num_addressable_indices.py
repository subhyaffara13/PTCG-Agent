
def num_addressable_indices(
    tensor_sharding: jsharding.Sharding, dim: int, global_shape: Shape) -> int:
  """Returns the number of indices for given dimension this host has access to.

  Each host can have multiple number of devices that are spanning
  possibly discontiguous slices of data. This function computes the
  total number of unique indices for dimension `dim` that any of its
  addressable devices hold.

  In most cases the addressable indices form a sparse grid (and in some
  cases a subcube), and thus each host will hold the same of number of
  indices for each dimension.  However, it is possible to design a mesh that
  addressable shards form a complicated pattern. In that case, the returned
  value is the number of indices that are addressable by at least one device.

  For example, suppose the sharding looks like this: (number indicates
  the host index)

    1221
    1221
    0000

  Then on host 1 and 2, both dim 0 (rows), and  dim=1 (cols) will have size 2,
  while on host 0, dim 0  will have size 1, and dim 1 will have size 4.

  Args:
    tensor_sharding: Sharding of the tensor.
    dim: dimension along which to compute the number of addressable indices.
    global_shape: global shape of the tensor.

  Returns:
    The number of indices for dimension  `dim` that this host holds.
  """
  # TODO(sandler, yashkatariya): Consider making this function public.
  addressables = tensor_sharding.addressable_devices_indices_map(global_shape)
  addressables = cast(Mapping[jsharding.Device, Index], addressables)
  num_unique_slices = len({
      _slice_as_tuple(addressable[dim]) for addressable in addressables.values()
  })
  shard_size = tensor_sharding.shard_shape(global_shape)[dim]
  return shard_size * num_unique_slices

