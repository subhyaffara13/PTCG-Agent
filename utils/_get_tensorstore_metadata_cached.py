
def _get_tensorstore_metadata_cached(
  global_shape: Sequence[int], dtype: jnp.dtype, local_shape: Sequence[int],
  is_remote: bool = False, file_size_target: int = _FILE_SIZE_TARGET,
  driver: str = _TS_ARRAY_DRIVER) -> dict[str, Any]:
  if driver == "zarr3":
    codecs = ([{"name": "zstd"}] if is_remote else [])
    return {
        'codecs': codecs,
        'shape': global_shape,
        'data_type': jnp.dtype(dtype).name,
        'chunk_grid': {
          'name': 'regular',
          'configuration': {'chunk_shape': _compute_chunk_shape(
              local_shape, dtype, file_size_target=file_size_target)}
        }
    }
  elif driver == "zarr":  # in zarr dtype goes in the base spec
    return {'compressor': {'id': 'zstd'}, 'shape': global_shape,
            'chunks': np.array(np.maximum(1, local_shape)).tolist()}
  else:
    raise ValueError(f"Unsupported driver: {driver}")

