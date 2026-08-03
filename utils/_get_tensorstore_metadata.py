from typing import Any

def _get_tensorstore_metadata(arr, is_remote: bool = False,
                              file_size_target: int = _FILE_SIZE_TARGET,
                              driver: str = _TS_ARRAY_DRIVER) -> dict[str, Any]:
  global_shape, dtype = arr.shape, arr.dtype
  if isinstance(arr, jax.Array):
    local_shape = arr.sharding.shard_shape(global_shape)
  else:  # np.ndarray
    local_shape = global_shape
  return _get_tensorstore_metadata_cached(global_shape, dtype, local_shape,
                                          is_remote, file_size_target, driver)

