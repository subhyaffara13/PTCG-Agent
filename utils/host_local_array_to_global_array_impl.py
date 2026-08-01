
def host_local_array_to_global_array_impl(
    arr: Any, *, global_mesh: jax.sharding.Mesh, pspec: Any):
  if pspec is None:
    raise ValueError(
        '`None` is not a valid input to the pspecs argument. Please use '
        'jax.sharding.PartitionSpec() if you wanted to replicate your input.')
  # If the Array is not fully addressable i.e. not host local, return it.
  if isinstance(arr, array.ArrayImpl) and not arr.is_fully_addressable:
    return arr
  if (isinstance(arr, array.ArrayImpl) and not hasattr(arr, 'shape')):
    arr = np.array(arr)
  if arr.dtype == dtypes.float0:
    arr = np.zeros(arr.shape, dtype=np.dtype(bool))
  dtype = arr.dtype
  if is_prng_key_array := isinstance(arr, prng.PRNGKeyArray):
    arr = arr._base_array

  local_sharding = jax.sharding.NamedSharding(global_mesh.local_mesh, pspec)

  # If the input is a concrete jax.Array and the input array sharding
  # matches the `local_sharding`, then there's no need to reshard and create
  # copies.
  if (isinstance(arr, array.ArrayImpl) and
      arr.sharding.is_equivalent_to(local_sharding, arr.ndim)):
    arrays = [x.data for x in arr.addressable_shards]
  else:
    arr = dtypes.canonicalize_value(arr)
    arrays = [
        arr[i] for i in local_sharding.devices_indices_map(arr.shape).values()
    ]

  global_aval = _local_to_global_aval(
      core.ShapedArray(arr.shape, arr.dtype), global_mesh, pspec)

  out = pxla.batched_device_put(
      global_aval, jax.sharding.NamedSharding(global_mesh, pspec),
      arrays, list(global_mesh.local_mesh.devices.flat))
  if is_prng_key_array:
    return prng.PRNGKeyArray(dtype._impl, out)
  return out

