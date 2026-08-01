
def array_metadata_from_tensorstore(
    t: Any,
    info: types.ParamInfo,
    sharding: sharding_metadata.ShardingMetadata | None = None,
) -> value_metadata.ArrayMetadata:
  return value_metadata.ArrayMetadata(
      name=info.name,
      directory=info.parent_dir,
      shape=t.shape,
      dtype=jnp.dtype(t.dtype.name),
      sharding=sharding,
      storage=value_metadata.StorageMetadata(
          chunk_shape=t.chunk_layout.read_chunk_template.shape,
          write_shape=info.write_shape,
      ),
  )

