
def global_array_to_host_local_array_impl(
    arr: Any, *, global_mesh: jax.sharding.Mesh, pspec: Any):
  if pspec is None:
    raise ValueError(
        '`None` is not a valid input to the pspecs argument. Please use '
        'jax.sharding.PartitionSpec() if you wanted to replicate your input.')
  # If the Array is already fully addressable i.e. host local, return it.
  if isinstance(arr, array.ArrayImpl) and arr.is_fully_addressable:
    return arr
  if not hasattr(arr, 'shape'):
    arr = np.array(arr)
  if arr.dtype == dtypes.float0:
    arr = np.zeros(arr.shape, dtype=np.dtype(bool))
  dtype = arr.dtype
  if is_prng_key_array := isinstance(arr, prng.PRNGKeyArray):
    arr = arr._base_array

  global_sharding = jax.sharding.NamedSharding(global_mesh, pspec)
  local_sharding = jax.sharding.NamedSharding(global_mesh.local_mesh, pspec)
  local_aval = _global_to_local_aval(
      core.ShapedArray(arr.shape, arr.dtype), global_mesh, pspec)

  if isinstance(arr, array.ArrayImpl):
    if arr.sharding.is_equivalent_to(global_sharding, arr.ndim):
      arrays = arr._arrays
    else:
      resharded_array = jax.device_put(arr, global_sharding)
      arrays = resharded_array._arrays
    out = array.ArrayImpl(local_aval, local_sharding, arrays, committed=True)
    if is_prng_key_array:
      return prng.PRNGKeyArray(dtype._impl, out)
    return out
  else:
    # numpy array can show up here during AD.
    arr = dtypes.canonicalize_value(arr)
    arrays = [
        arr[i] for i in local_sharding.devices_indices_map(arr.shape).values()
    ]
  return pxla.batched_device_put(
      local_aval, local_sharding, arrays,
      list(global_mesh.local_mesh.devices.flat))

