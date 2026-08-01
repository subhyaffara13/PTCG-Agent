
def is_pytree_checkpoint(path: epath.Path) -> bool:
  return (
      _has_pytree_metadata_file(path) and _has_tensorstore_data_files(path)
  ) or (
      _has_msgpack_metadata_file(path)
      and all([not x for x in _has_zarray_files(path)])
  )

